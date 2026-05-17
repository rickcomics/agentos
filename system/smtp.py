import smtplib
from email.mime.text import MIMEText
from system.config import load_env

def send_email(to, subject, body, from_email):
    env = load_env()

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to

    with smtplib.SMTP_SSL(env["SMTP_HOST"], int(env["SMTP_PORT"])) as server:
        server.login(env["SMTP_USER"], env["SMTP_PASSWORD"])
        server.sendmail(from_email, [to], msg.as_string())

    print(f"[SMTP] Письмо отправлено → {to}")
