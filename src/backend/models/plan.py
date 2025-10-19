from pydantic import BaseModel, Field, ConfigDict


class FinancingPlan(BaseModel):
    """Modelo para validar datos de planes de financiación"""

    name: str = Field(..., min_length=1, max_length=100, description="Nombre del plan")
    rate: str = Field(..., min_length=1, max_length=20, description="Tasa de interés")
    rateLabel: str = Field(
        ..., min_length=1, max_length=50, description="Etiqueta de la tasa"
    )
    months: int = Field(..., gt=0, le=360, description="Plazo en meses")
    downPayment: int = Field(..., ge=0, le=100, description="Porcentaje de anticipo")

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "name": "Plan Flexible",
                "rate": "15%",
                "rateLabel": "T.N.A",
                "months": 48,
                "downPayment": 20,
            }
        },
    )
