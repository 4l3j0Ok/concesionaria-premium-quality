from models.car import Car, CarCreate, CarFeatures
from sqlmodel import select, Session
from typing import List, Optional
from fastapi import HTTPException
import requests
from PIL import Image
from io import BytesIO
import os
from core.config import AppConfig


class CarController:
    @staticmethod
    def _save_image_as_file(image_bytes: bytes, car_code: str) -> str:
        """Guarda la imagen como archivo WebP y retorna la URL"""
        try:
            # Crear directorio de imágenes si no existe
            images_dir = os.path.join(AppConfig.STATIC_DIR, "images")
            os.makedirs(images_dir, exist_ok=True)

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

            # Generar nombre de archivo único basado en car_code
            filename = f"{car_code}.webp"
            filepath = os.path.join(images_dir, filename)

            # Guardar como WebP
            img.save(filepath, format="WEBP", quality=85, method=6)

            # Retornar la URL pública
            return f"{AppConfig.STATIC_URL}/images/{filename}"
        except Exception as e:
            print(f"Error al guardar imagen: {e}")
            raise HTTPException(
                status_code=500, detail=f"Error al procesar la imagen: {str(e)}"
            )

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
        # Convertir features a modelo en todos los coches
        cars_serialized = []
        for car in cars:
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
                    # Guardar imagen como archivo y obtener URL
                    car_data["image"] = CarController._save_image_as_file(
                        response.content, car.car_code
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
        # Convertir features a modelo antes de devolver
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
        # Convertir features a modelo antes de devolver
        car = CarController._convert_features_to_model(car)
        return car

    @staticmethod
    def delete_car(session: Session, car_id: int) -> None:
        car = session.get(Car, car_id)
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")
        session.delete(car)
        session.commit()
