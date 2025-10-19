from models.car import Car, CarCreate, CarFeatures
from sqlmodel import select, Session
from typing import List, Optional
from fastapi import HTTPException
import requests
import base64
from PIL import Image
from io import BytesIO


class CarController:
    @staticmethod
    def _convert_image_to_webp(image_bytes: bytes) -> bytes:
        """Convierte una imagen a formato WebP para optimizar el tamaño"""
        try:
            # Abrir la imagen desde bytes
            img = Image.open(BytesIO(image_bytes))

            # Convertir a RGB si es necesario (WebP no soporta algunos modos)
            if img.mode in ("RGBA", "LA", "P"):
                # Crear fondo blanco para transparencias
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(
                    img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None
                )
                img = background
            elif img.mode != "RGB":
                img = img.convert("RGB")

            # Guardar como WebP en memoria
            output = BytesIO()
            img.save(output, format="WEBP", quality=85, method=6)
            return output.getvalue()
        except Exception as e:
            # Si falla la conversión, devolver la imagen original
            print(f"Error al convertir imagen a WebP: {e}")
            return image_bytes

    @staticmethod
    def _convert_image_to_base64(car: Car) -> Car:
        """Convierte la imagen de bytes a base64 para la respuesta"""
        if car.image and isinstance(car.image, bytes):
            car.image = base64.b64encode(car.image).decode("utf-8")
        return car

    @staticmethod
    def _convert_features_to_model(car: Car) -> Car:
        """Convierte el dict de features a CarFeatures si es necesario"""
        if car.features and isinstance(car.features, dict):
            car.features = CarFeatures(**car.features)
        return car

    @staticmethod
    def get_cars(
        session: Session,
        car_code: Optional[str] = None,
        brand: Optional[str] = None,
        model: Optional[str] = None,
        year: Optional[int] = None,
        offset: int = 0,
        limit: int = 100,
    ) -> List[Car]:
        query = select(Car)
        if car_code:
            query = query.where(Car.car_code == car_code)
        if brand:
            query = query.where(Car.brand.contains(brand))
        if model:
            query = query.where(Car.model.contains(model))
        if year:
            query = query.where(Car.year == year)
        cars = session.exec(query.offset(offset).limit(limit)).all()
        # Convertir bytes a base64 y features a modelo en todas los coches
        cars_serialized = []
        for car in cars:
            car = CarController._convert_image_to_base64(car)
            car = CarController._convert_features_to_model(car)
            cars_serialized.append(car)
        return cars_serialized

    @staticmethod
    def create_car(session: Session, car: CarCreate) -> Car:
        existing_car = session.exec(
            select(Car).where(Car.car_code == car.car_code)
        ).first()
        if existing_car:
            raise HTTPException(
                status_code=409,
                detail=f"El código del vehículo '{car.car_code}' ya existe.",
            )

        # Primero obtener los datos del modelo
        car_data = car.model_dump()

        # Convertir features a dict si existe
        if car_data.get("features") and hasattr(car_data["features"], "model_dump"):
            car_data["features"] = car_data["features"].model_dump()

        # Procesar la imagen después de hacer model_dump
        if car.image:
            response = requests.get(str(car.image))
            if response.status_code == 200:
                content_type = response.headers.get("Content-Type", "")
                if content_type.startswith("image/"):
                    # Convertir a WebP para optimizar tamaño
                    car_data["image"] = CarController._convert_image_to_webp(
                        response.content
                    )
                else:
                    raise HTTPException(
                        status_code=400,
                        detail="La URL proporcionada no contiene una imagen válida.",
                    )
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"No se pudo descargar la imagen. Status code: {response.status_code}",
                )

        car = Car(**car_data)
        session.add(car)
        session.commit()
        session.refresh(car)
        # Convertir bytes a base64 y features a modelo antes de devolver
        car = CarController._convert_image_to_base64(car)
        car = CarController._convert_features_to_model(car)
        return car

    @staticmethod
    def update_car(session: Session, car_id: int, car_data: Car) -> Car:
        car = session.get(Car, car_id)
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")
        for key, value in car_data.model_dump(exclude_unset=True).items():
            setattr(car, key, value)
        session.add(car)
        session.commit()
        session.refresh(car)
        # Convertir bytes a base64 y features a modelo antes de devolver
        car = CarController._convert_image_to_base64(car)
        car = CarController._convert_features_to_model(car)
        return car

    @staticmethod
    def delete_car(session: Session, car_id: int) -> None:
        car = session.get(Car, car_id)
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")
        session.delete(car)
        session.commit()
