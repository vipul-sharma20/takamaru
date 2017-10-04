import base64
import configparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import Celery

from constants import SMTP_SERVER, SMTP_PORT, CONFIG_FILE

app = Celery('tasks', backend='amqp', broker='amqp://')


@app.task
def send_email(subject, body, recipients):
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    gmail_user = config['GMAIL']['USER']
    gmail_pwd = base64.b64decode(config['GMAIL']['PASSWORD']).decode('UTF-8')
    print("sending email")
    try:
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()

        server.login(gmail_user, gmail_pwd)
        text = msg.as_string()
        server.sendmail(gmail_user, recipients, text)
        server.quit()
        print("Email sent")
    except smtplib.SMTPException:
        print("Failed to send email")

