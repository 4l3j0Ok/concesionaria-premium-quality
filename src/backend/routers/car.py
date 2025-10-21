from fastapi import APIRouter, Depends, HTTPException, Query, Response
from typing import Annotated
from controllers.car import CarController
from core import db
from models.car import CarCreate, CarResponse

# API ROUTER CLASIFICADO EN DOCS
router = APIRouter(
    tags=["cars"],
)


@router.get("/cars", response_model=CarResponse)
def get_cars(
    response: Response,
    session: Annotated[db.Session, Depends(db.get_session)],
    code: Annotated[
        str | None, Query(description="Filtrar por código del vehículo")
    ] = None,
    brand: Annotated[str | None, Query(description="Filtrar por marca")] = None,
    model: Annotated[str | None, Query(description="Filtrar por modelo")] = None,
    year: Annotated[int | None, Query(description="Filtrar por año")] = None,
    offset: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(
        100, ge=1, le=1000, description="Número máximo de registros a devolver"
    ),
):
    # Añadir headers de caché para mejorar rendimiento
    response.headers["Cache-Control"] = "public, max-age=300"  # 5 minutos de caché

    cars = CarController.get_cars(
        session=session,
        code=code,
        brand=brand,
        model=model,
        year=year,
        offset=offset,
        limit=limit,
    )
    return CarResponse(total=len(cars), offset=offset, limit=limit, items=cars)


@router.post("/cars", response_model=CarResponse)
def create_car(car: CarCreate, session: Annotated[db.Session, Depends(db.get_session)]):
    try:
        new_car = CarController.create_car(session, car)
        return CarResponse(total=1, offset=0, limit=1, items=[new_car])
    except HTTPException as e:
        raise e


@router.put("/cars/{car_id}", response_model=CarResponse)
def update_car(
    car_id: int,
    car_data: CarCreate,
    session: Annotated[db.Session, Depends(db.get_session)],
):
    updated_car = CarController.update_car(session, car_id, car_data)
    return CarResponse(total=1, offset=0, limit=1, items=[updated_car])


@router.delete("/cars/{car_id}", status_code=204)
def delete_car(
    car_id: int,
    session: Annotated[db.Session, Depends(db.get_session)],
):
    CarController.delete_car(session, car_id)
    return
