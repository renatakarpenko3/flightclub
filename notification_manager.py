import smtplib
from twilio.rest import Client

MY_MAIL_PROVIDER_SMTP_ADDRESS = "EMAIL PROVIDER SMTP ADDRESS"
MY_MY_EMAIL = "EMAIL"
MY_MY_PASSWORD = "PASSWORD"
MY_TWILIO_SID = "TWILIO ACCOUNT SID"
MY_TWILIO_AUTH_TOKEN = "TWILIO AUTH TOKEN"
MY_TWILIO_VIRTUAL_NUMBER = "TWILIO VIRTUAL NUMBER"
MY_TWILIO_VERIFIED_NUMBER = "TWILIO VERIFIED NUMBER"


class MyCustomNotificationService:

    def __init__(self):
        self.client = Client(MY_TWILIO_SID, MY_TWILIO_AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=MY_TWILIO_VIRTUAL_NUMBER,
            to=MY_TWILIO_VERIFIED_NUMBER,
        )
        print(message.sid)

    def send_emails(self, emails, message):
        with smtplib.SMTP(MY_MAIL_PROVIDER_SMTP_ADDRESS) as connection:
            connection.starttls()
            connection.login(MY_MY_EMAIL, MY_MY_PASSWORD)
            for email in emails:
                connection.sendmail(
                    from_addr=MY_MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}".encode('utf-8')
                )