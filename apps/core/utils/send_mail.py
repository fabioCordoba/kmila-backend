from django.conf import settings
import sendgrid
from sendgrid.helpers.mail import Mail


def send_email(to_email, subject, content):
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

    message = Mail(
        from_email="airihsrecker@gmail.com",  # remitente verificado en SendGrid
        to_emails=to_email,
        subject=subject,
        plain_text_content=content,
    )

    try:
        response = sg.send(message)
        return {
            "status": response.status_code,
            "body": response.body.decode("utf-8") if response.body else None,
        }
    except Exception as e:
        return {"error": str(e)}
