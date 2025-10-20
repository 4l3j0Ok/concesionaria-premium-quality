from pydantic import AnyUrl, BaseModel, computed_field
from typing import Optional, List, Union
from sqlmodel import SQLModel, Field, UniqueConstraint, Column
from sqlalchemy import JSON


# Modelos de características simplificados
class CarFeatures(BaseModel):
    """Características del vehículo"""

    fuel_type: Optional[str] = Field(
        default=None,
        description="Tipo de combustible (Nafta, Diésel, Eléctrico, Híbrido)",
    )
    transmission: Optional[str] = Field(
        default=None, description="Tipo de transmisión (Manual, Automática, CVT)"
    )
    body_type: Optional[str] = Field(
        default=None, description="Tipo de carrocería (Sedán, Hatchback, SUV, Pickup)"
    )
    passengers: Optional[int] = Field(
        default=None, ge=1, le=9, description="Capacidad de pasajeros"
    )
    doors: Optional[int] = Field(
        default=None, ge=2, le=5, description="Número de puertas"
    )
    air_conditioning: Optional[bool] = Field(
        default=None, description="Tiene aire acondicionado"
    )
    airbags: Optional[int] = Field(default=None, ge=0, description="Número de airbags")
    abs: Optional[bool] = Field(default=None, description="Sistema de frenos ABS")


# Base con validaciones (sin features)
class CarBase(SQLModel):
    brand: str = Field(min_length=1, max_length=50, description="Marca del vehículo")
    model: str = Field(min_length=1, max_length=50, description="Modelo del vehículo")
    description: str = Field(
        min_length=1, description="Descripción detallada del vehículo"
    )
    price: float = Field(gt=0, description="Precio base del vehículo")
    promotion_price: Optional[float] = Field(
        default=None, gt=0, description="Precio promocional si está disponible"
    )
    km: int = Field(ge=0, description="Kilómetros recorridos del vehículo")
    year: int = Field(ge=1886, le=2100, description="Año de fabricación")
    image: Optional[Union[AnyUrl, bytes]] = Field(
        default=None, description="URL de la imagen del vehículo"
    )


# Modelo de creación (input del POST)
class CarCreate(CarBase):
    features: Optional[CarFeatures] = Field(
        default=None, description="Características del vehículo"
    )

    @computed_field
    @property
    def car_code(self) -> str:
        return f"{self.brand.lower()}-{self.model.lower()}"


class CarRead(CarBase):
    id: int
    car_code: str
    image: Optional[str] = Field(
        default=None, description="URL de la imagen del vehículo"
    )
    features: Optional[CarFeatures] = Field(
        default=None, description="Características del vehículo"
    )

    model_config = {"from_attributes": True}


class CarResponse(BaseModel):
    total: int
    offset: int
    limit: int
    items: List[CarRead]  # ahora usamos CarRead con from_attributes


# Modelo de tabla (DB)
class Car(CarBase, table=True):
    __tablename__ = "car"
    __table_args__ = (
        UniqueConstraint("car_code", name="uq_car_code"),
        {"extend_existing": True},
    )
    car_code: str = Field(
        min_length=1, max_length=50, description="Código único del vehículo"
    )
    image: Optional[str] = Field(
        default=None,
        description="Nombre del archivo de imagen (guardado en /static/data)",
    )
    features: Optional[dict] = Field(
        default=None, sa_column=Column(JSON), description="Características del vehículo"
    )
    id: Optional[int] = Field(default=None, primary_key=True)
