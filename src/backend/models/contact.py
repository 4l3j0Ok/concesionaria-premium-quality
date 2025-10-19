from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING
from models.plan import FinancingPlan


class CarContactData(BaseModel):
    """Modelo para validar datos del auto en el contacto"""

    code: str = Field(..., min_length=1, max_length=100, description="Código del auto")
    brand: str = Field(
        ..., min_length=1, max_length=50, description="Marca del vehículo"
    )
    model: str = Field(
        ..., min_length=1, max_length=50, description="Modelo del vehículo"
    )
    year: int = Field(..., ge=1886, le=2100, description="Año de fabricación")
    km: int = Field(..., ge=0, description="Kilómetros recorridos")
    price: float = Field(..., gt=0, description="Precio del vehículo")
    img: Optional[str] = Field(
        default=None, description="URL de la imagen del vehículo"
    )


class ContactRequest(BaseModel):
    """Modelo para el request de contacto"""

    contact_name: str = Field(
        ..., min_length=1, max_length=100, description="Nombre del remitente"
    )
    contact_email: str = Field(..., description="Email del remitente")
    contact_message: str = Field(..., min_length=1, description="Mensaje del remitente")
    car_data: Optional[CarContactData] = Field(
        default=None, description="Datos del auto consultado"
    )
    plan_data: Optional[FinancingPlan] = Field(
        default=None,
        description="Datos del plan consultado (validado como FinancingPlan)",
    )
