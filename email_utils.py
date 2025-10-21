import smtplib
from email.mime.text import MIMEText

def send_email_app_password(to_email, subject, body, sender_email, app_password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, to_email, msg.as_string())
