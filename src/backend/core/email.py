from core.config import EmailConfig
import resend


def send_email(to_email: str, subject: str, html_content: str):
    resend.api_key = EmailConfig.RESEND_API_KEY
    params: resend.Emails.SendParams = {
        "to": to_email,
        "from": EmailConfig.FROM_EMAIL,
        "subject": subject,
        "html": html_content,
    }
    email: resend.Email = resend.Emails.send(params)
    return email
