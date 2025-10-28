from models.car import Car, CarCreate, CarFeatures
from sqlmodel import select, Session
from typing import List, Optional
from fastapi import HTTPException
import requests
from PIL import Image
from io import BytesIO
import os
import uuid
from core.config import AppConfig


class CarController:
    @staticmethod
    def _ensure_images_directory():
        """Asegura que el directorio de imágenes existe"""
        os.makedirs(AppConfig.IMAGES_DIR, exist_ok=True)

    @staticmethod
    def _save_image_to_file(image_bytes: bytes, code: str) -> str:
        """Guarda la imagen en el sistema de archivos y retorna el nombre del archivo"""
        CarController._ensure_images_directory()

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

            # Generar nombre de archivo único
            filename = f"{code}_{uuid.uuid4().hex[:8]}.webp"
            filepath = os.path.join(AppConfig.IMAGES_DIR, filename)

            # Guardar como WebP con calidad optimizada
            img.save(filepath, format="WEBP", quality=85, method=6)

            return filename
        except Exception as e:
            print(f"Error al guardar imagen: {e}")
            raise HTTPException(
                status_code=500, detail=f"Error al procesar la imagen: {str(e)}"
            )

    @staticmethod
    def _delete_image_file(filename: str):
        """Elimina una imagen del sistema de archivos"""
        if filename:
            filepath = os.path.join(AppConfig.IMAGES_DIR, filename)
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except Exception as e:
                    print(f"Error al eliminar imagen {filename}: {e}")

    @staticmethod
    def _convert_image_to_url(car: Car) -> Car:
        """Convierte el nombre del archivo de imagen a URL completa"""
        if car.image:
            car.image = f"{AppConfig.IMAGES_URL}/{car.image}"
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
        code: Optional[str] = None,
        search: Optional[str] = None,
        brand: Optional[str] = None,
        model: Optional[str] = None,
        year: Optional[int] = None,
        offset: int = 0,
        limit: int = 100,
    ) -> List[Car]:
        query = select(Car)
        if search:
            search_term = f"%{search}%"
            query = query.where(
                (Car.brand.ilike(search_term)) | (Car.model.ilike(search_term))
            )
        if code:
            query = query.where(Car.code == code)
        if brand:
            query = query.where(Car.brand.contains(brand))
        if model:
            query = query.where(Car.model.contains(model))
        if year:
            query = query.where(Car.year == year)
        cars = session.exec(query.offset(offset).limit(limit)).all()
        # Convertir filename a URL y features a modelo en todos los coches
        cars_serialized = []
        for car in cars:
            car = CarController._convert_image_to_url(car)
            car = CarController._convert_features_to_model(car)
            cars_serialized.append(car)
        return cars_serialized

    @staticmethod
    def create_car(session: Session, car: CarCreate) -> Car:
        existing_car = session.exec(select(Car).where(Car.code == car.code)).first()
        if existing_car:
            raise HTTPException(
                status_code=409,
                detail=f"El código del vehículo '{car.code}' ya existe.",
            )

        # Primero obtener los datos del modelo
        car_data = car.model_dump()

        # Convertir features a dict si existe
        if car_data.get("features") and hasattr(car_data["features"], "model_dump"):
            car_data["features"] = car_data["features"].model_dump()

        # Procesar la imagen: descargar y guardar en el sistema de archivos
        if car.image:
            response = requests.get(str(car.image))
            if response.status_code == 200:
                content_type = response.headers.get("Content-Type", "")
                if content_type.startswith("image/"):
                    # Guardar imagen en el sistema de archivos
                    filename = CarController._save_image_to_file(
                        response.content, car.code
                    )
                    car_data["image"] = filename
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
        # Convertir filename a URL y features a modelo antes de devolver
        car = CarController._convert_image_to_url(car)
        car = CarController._convert_features_to_model(car)
        return car

    @staticmethod
    def update_car(session: Session, car_id: int, car_data: CarCreate) -> Car:
        car = session.get(Car, car_id)
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")

        # Guardar el nombre de imagen anterior para eliminarlo si se actualiza
        old_image = car.image

        # Obtener los datos del modelo
        update_data = car_data.model_dump(exclude_unset=True)

        # Convertir features a dict si existe
        if update_data.get("features") and hasattr(
            update_data["features"], "model_dump"
        ):
            update_data["features"] = update_data["features"].model_dump()

        # Procesar la imagen si se proporciona una nueva URL
        if "image" in update_data and update_data["image"]:
            response = requests.get(str(update_data["image"]))
            if response.status_code == 200:
                content_type = response.headers.get("Content-Type", "")
                if content_type.startswith("image/"):
                    # Guardar imagen en el sistema de archivos
                    filename = CarController._save_image_to_file(
                        response.content, car.code
                    )
                    update_data["image"] = filename
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

        # Actualizar campos
        for key, value in update_data.items():
            setattr(car, key, value)

        # Si se actualizó la imagen, eliminar la anterior
        if old_image and car.image != old_image:
            CarController._delete_image_file(old_image)

        session.add(car)
        session.commit()
        session.refresh(car)
        # Convertir filename a URL y features a modelo antes de devolver
        car = CarController._convert_image_to_url(car)
        car = CarController._convert_features_to_model(car)
        return car

    @staticmethod
    def delete_car(session: Session, car_id: int) -> None:
        car = session.get(Car, car_id)
        if not car:
            raise HTTPException(status_code=404, detail="Car not found")

        # Eliminar la imagen del sistema de archivos
        if car.image:
            CarController._delete_image_file(car.image)

        session.delete(car)
        session.commit()
