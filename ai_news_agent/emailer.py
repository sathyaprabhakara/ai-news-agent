import smtplib
from email.message import EmailMessage
from .config import cfg
import logging

logger = logging.getLogger(__name__)


def send_email(subject: str, body: str) -> bool:
    if not cfg.EMAIL_FROM or not cfg.EMAIL_PASSWORD or not cfg.EMAIL_TO:
        logger.warning("Email credentials or addresses not set; skipping email send")
        return False

    msg = EmailMessage()
    msg["From"] = cfg.EMAIL_FROM
    msg["To"] = cfg.EMAIL_TO
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        logger.info("Sending email to %s", cfg.EMAIL_TO)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(cfg.EMAIL_FROM, cfg.EMAIL_PASSWORD)
            smtp.send_message(msg)
        logger.info("Email sent")
        return True
    except Exception as e:
        logger.exception("Failed to send email: %s", e)
        return False
