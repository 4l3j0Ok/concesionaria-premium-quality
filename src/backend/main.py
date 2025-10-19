from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from core import db
from core.config import AppConfig
from routers import car, contact
import uvicorn


app = FastAPI(
    title=AppConfig.TITLE,
    description=AppConfig.DESCRIPTION,
    version=AppConfig.VERSION,
    debug=AppConfig.DEBUG,
)

app.include_router(car.router)
app.include_router(contact.router)
app.mount(
    AppConfig.STATIC_URL,
    StaticFiles(directory=AppConfig.STATIC_DIR),
    name="static",
)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    db.create_db_and_tables()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
