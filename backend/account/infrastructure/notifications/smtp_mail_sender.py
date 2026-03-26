import smtplib
from email.mime.text import MIMEText

from app.config import settings


class SMTPMailSender:
    def send_code(self, code: int, to_email: str) -> None:
        subject = 'Подтверждение регистрации'
        body = f'Ваш код подтверждения: {code}'

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = settings.email_login
        msg['To'] = to_email

        with smtplib.SMTP_SSL(
            settings.smtp_host, settings.smtp_port, timeout=10
        ) as server:
            server.login(settings.email_login, settings.email_password)
            server.send_message(msg)
