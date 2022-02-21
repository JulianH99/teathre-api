import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .config import MAIL_HOST, MAIL_PORT, MAIL_PASS, MAIL_USER

smtp = smtplib.SMTP(MAIL_HOST, MAIL_PORT)
smtp.connect(MAIL_HOST, MAIL_PORT)

smtp.ehlo()
smtp.starttls()
smtp.ehlo()

smtp.login(MAIL_USER, MAIL_PASS)


def send_mail(to, subject, message):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'Equipo de teatro'
    msg['To'] = to

    msg.attach(MIMEText(message, 'html'))

    smtp.sendmail(MAIL_USER, to, msg.as_string())
