from fastapi_mail import (
    FastMail,
    MessageSchema,
    ConnectionConfig,
    MessageType
)

from src.config.setting import settings


config = ConnectionConfig(
    MAIL_USERNAME=settings.MAILTRAP_USERNAME,
    MAIL_PASSWORD=settings.MAILTRAP_PASSWORD,
    MAIL_PORT=settings.MAILTRAP_PORT,
    MAIL_SERVER="sandbox.smtp.mailtrap.io",
    MAIL_FROM=settings.APP_EMAIL,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)


def schema(to, otp):
    return MessageSchema(
        recipients=[to],
        subject="OTP for verification",
        body=f"""
        <h2>Welcome!</h2>
        <p>Your verification OTP is:</p>
        <h1>{otp}</h1>
        """,
        subtype=MessageType.html
    )


async def send_email(to, otp):
    message = schema(to, otp)

    fm = FastMail(config)

    await fm.send_message(message)