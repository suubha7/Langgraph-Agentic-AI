import os
import imaplib
import smtplib
import email
from email.header import decode_header
from email.message import EmailMessage
from dotenv import load_dotenv
import re

load_dotenv()

class EmailClient:
    def __init__(self):
        self.EMAIL = os.getenv("EMAIL")
        self.APP_PASSWORD = os.getenv("APP_PASSWORD")
        self.IMAP_SERVER = "imap.gmail.com"
        self.SMTP_SERVER = "smtp.gmail.com"
        self.SMTP_PORT = 465

    def receive_email(self):
        mail = imaplib.IMAP4_SSL(self.IMAP_SERVER)
        mail.login(self.EMAIL, self.APP_PASSWORD)
        mail.select("inbox")

        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()

        if not email_ids:
            mail.logout()
            return None

        latest_id = email_ids[-1]

        status, msg_data = mail.fetch(latest_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        # Decode subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        # Extract sender email
        raw_sender = msg.get("From")
        match = re.search(r'<(.+?)>', raw_sender)
        sender = match.group(1) if match else raw_sender

        # Extract body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()

        mail.logout()

        return {
            "email_id": latest_id,
            "sender": sender,
            "subject": subject,
            "body": body
        }


    def send_email(self, to, subject, body):
        msg = EmailMessage()
        msg["From"] = self.EMAIL
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)

        with smtplib.SMTP_SSL(self.SMTP_SERVER, self.SMTP_PORT) as server:
            server.login(self.EMAIL, self.APP_PASSWORD)
            server.send_message(msg)

        return "Email sent successfully"

    def delete_email(self, email_id):
        mail = imaplib.IMAP4_SSL(self.IMAP_SERVER)
        mail.login(self.EMAIL, self.APP_PASSWORD)
        mail.select("inbox")

        mail.store(email_id, "+FLAGS", "\\Deleted")
        mail.expunge()
        mail.logout()

        return "Email deleted"