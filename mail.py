from email.mime.base import MIMEBase
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.encoders import encode_base64

from config import MAIL_HOST, MAIL_PORT, MAIL_PASS, MAIL_USER


def send_mail(to, subject, message, attachment_string=None):
    smtp = smtplib.SMTP(MAIL_HOST, MAIL_PORT)
    smtp.connect(MAIL_HOST, MAIL_PORT)

    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(MAIL_USER, MAIL_PASS)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'Equipo de teatro'
    msg['To'] = to

    if attachment_string:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment_string)
        encode_base64(part)

        part.add_header('Content-Disposition',
                        'attachment; filename="{}.pdf"'.format(to))

    msg.attach(part)

    msg.attach(MIMEText(message, 'html'))

    smtp.sendmail(MAIL_USER, to, msg.as_string())
