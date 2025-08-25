from celery import shared_task
from django.utils import timezone

from apps.core.utils.send_mail import send_email
from apps.loan.models.loan import Loan


@shared_task
def accrue_interest():
    today = timezone.now().date()
    day_number = today.day
    loans = Loan.objects.filter(status="active")

    for loan in loans:
        if loan.start_date.day == day_number:
            # Calcular interés mensual simple (puedes ajustar fórmula)
            monthly_interest = (loan.capital_balance * loan.interest_rate) / 100

            loan.interest_balance += monthly_interest
            loan.save(update_fields=["interest_balance"])

            # Enviar correo al cliente
            subject = "Actualización de tu préstamo"
            message = (
                f"Hola {loan.client.first_name},\n\n"
                f"Se ha aplicado un interés mensual de ${monthly_interest:,.2f} "
                f"a tu préstamo con codigo {loan.code}.\n\n"
                f"Tu nuevo saldo de intereses es: ${loan.interest_balance:,.2f}.\n"
                f"Tu saldo de capital es: ${loan.capital_balance:,.2f}.\n\n"
                "Por favor mantente al día con tus pagos."
            )
            recipient = loan.client.email
            try:
                response = send_email(
                    recipient,
                    subject,
                    message,
                )
                print(response)
                print(f"Correo enviado a {loan.client.email}")
            except Exception as e:
                print(f"Error enviando correo a {loan.client.email}: {e}")
