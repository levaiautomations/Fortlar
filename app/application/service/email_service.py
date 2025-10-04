import smtplib
import ssl
from email.message import EmailMessage
from loguru import logger

import envs


class EmailService:
    def __init__(self):
        self.username = envs.MAIL_USERNAME
        self.password = envs.MAIL_PASSWORD
        self.mail_from = envs.MAIL_FROM
        self.mail_server = envs.MAIL_SERVER
        self.mail_port = envs.MAIL_PORT
        self.use_tls = True

    def send_email(self, recipient: str, template_html: str, subject: str):
        try:
            # Monta mensagem
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = self.mail_from or self.username
            msg["To"] = recipient
            msg.set_content("Seu cliente de email não suporta HTML.")
            msg.add_alternative(template_html, subtype="html")

            # Contexto SSL
            context = ssl.create_default_context()

            # Decide entre SSL e TLS
            if self.mail_port == 465:
                with smtplib.SMTP_SSL(self.mail_server, self.mail_port, context=context) as server:
                    server.login(self.username, self.password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(self.mail_server, self.mail_port) as server:
                    if self.use_tls:
                        server.starttls(context=context)
                    server.login(self.username, self.password)
                    server.send_message(msg)

            logger.info(f"✅ Email enviado para {recipient}")

        except Exception as e:
            logger.error(f"❌ Erro ao enviar email: {e}")
            raise
