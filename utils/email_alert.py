
import smtplib
from email.mime.text import MIMEText

def send_email_alert(receiver_email, timestamps):
    sender_email = "projectmajorvd25@gmail.com"
    sender_password = "Ap10@w0667"

    subject = "Violence Detected Alert"
    body = f"Violence detected at timestamps (seconds): {timestamps}"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
