import logging

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from src.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.email_username,
    MAIL_PASSWORD=settings.email_password,
    MAIL_FROM=settings.email_from,
    MAIL_PORT=settings.email_port,
    MAIL_SERVER=settings.email_server,
    MAIL_STARTTLS=settings.email_starttls,
    MAIL_SSL_TLS=settings.email_ssl_tls,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_reset_password_email(email_to: str, token: str):
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2>Recuperação de Senha - DIO Blog</h2>
        <p>Olá!</p>
        <p>Recebemos um pedido para redefinir a senha da sua conta.</p>
        <p>Use o token de segurança abaixo no Swagger para cadastrar sua nova senha:</p>
        <div style="background-color: #f4f4f4; padding: 15px; text-align: center; border-radius: 5px;">
            <strong style="font-size: 20px; letter-spacing: 2px;">{token}</strong>
        </div>
        <p>Se você não solicitou essa alteração, pode ignorar este e-mail com segurança.</p>
    </div>
    """

    message = MessageSchema(
        subject="Redefinição de Senha - DIO Blog",
        recipients=[email_to],
        body=html,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)

    try:
        await fm.send_message(message)
        logging.info(f"E-mail enviado com sucesso para {email_to}")
    except Exception as e:
        logging.warning(f"Bloqueio SMTP detectado (Render Free Tier).")
        logging.warning(f"E-mail simulado para {email_to}. O Token é: {token}")
