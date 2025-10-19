from fastapi import APIRouter, HTTPException, Body
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from core import email
from core.config import EmailConfig
from core.logger import logger
from models.contact import ContactRequest


router = APIRouter(
    tags=["contact"],
)

# Configurar Jinja2
templates_dir = Path(__file__).parent.parent / "templates"
jinja_env = Environment(
    loader=FileSystemLoader(templates_dir),
    autoescape=select_autoescape(["html", "xml"]),
)


@router.post("/contact", status_code=204)
def send_contact_email(request: ContactRequest = Body(...)):
    try:
        # Preparar datos para los templates
        car_data_for_template = (
            request.car_data.model_dump() if request.car_data else None
        )
        plan_data_for_template = (
            request.plan_data.model_dump() if request.plan_data else None
        )

        # Renderizar template para la empresa
        company_template = jinja_env.get_template("email_to_company.html")
        company_html = company_template.render(
            contact_name=request.contact_name,
            contact_email=request.contact_email,
            contact_message=request.contact_message,
            car=car_data_for_template,
            plan=plan_data_for_template,
        )

        # Enviar email a la empresa
        subject = f"Nuevo mensaje de contacto de {request.contact_name}"
        result = email.send_email(
            to_email=EmailConfig.TO_EMAIL,
            subject=subject,
            html_content=company_html,
        )
        if not result.get("id"):
            raise HTTPException(
                status_code=500, detail="No se pudo enviar el correo electrónico."
            )

        # Renderizar template para el cliente
        customer_template = jinja_env.get_template("email_to_customer.html")
        customer_html = customer_template.render(
            contact_name=request.contact_name,
            contact_email=request.contact_email,
            contact_message=request.contact_message,
            car=car_data_for_template,
            plan=plan_data_for_template,
        )

        # Enviar correo de confirmación al cliente
        confirmation_subject = "Hemos recibido tu mensaje de contacto"
        email.send_email(
            to_email=request.contact_email,
            subject=confirmation_subject,
            html_content=customer_html,
        )
    except Exception as e:
        logger.error("Error al enviar el correo electrónico de contacto.")
        logger.exception(e)
        raise HTTPException(
            status_code=500, detail="Error al enviar el correo electrónico."
        ) from e
