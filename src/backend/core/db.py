import os
from core.logger import logger
from sqlmodel import create_engine, SQLModel, Session, inspect
from models.car import Car

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# Permite conexiones desde múltiples hilos (útil en aplicaciones web).
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def get_session():
    """
    Dependencia de FastAPI para obtener una sesión de base de datos.
    Esta función se usa cuando se necesita interactuar con la base de datos
    en las rutas de la API, principalmente en operaciones `CRUD` para asegurar
    que cada solicitud tenga su propia sesión de base de datos.
    """
    with Session(engine) as session:
        yield session


def create_db_and_tables(drop_existing: bool = False):
    """Crear la base de datos y todas las tablas."""
    if drop_existing:
        SQLModel.metadata.drop_all(engine)
    first_time = not inspect(engine).has_table(Car.__tablename__)
    if first_time:
        logger.info("Creando todas las tablas en la base de datos.")
        SQLModel.metadata.create_all(engine)


# Función para inicializar la base de datos con datos de ejemplo
def init_db():
    """Inicializar la base de datos con datos de ejemplo."""
    # Crear las tablas
    drop_db = os.getenv("CLEAR_DB_ON_STARTUP", "False").lower() == "true"
    create_db_and_tables(drop_existing=drop_db)
