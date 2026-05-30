import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

def send_welcome_email(receiver_email : str, username : str):

    sender_email = os.getenv("EMAIL")
    sender_password = os.getenv("APP_PASSWORD")

    subject = "Welcome to Modern Dairy"

    body = f"""
        Hello {username},

        Now u can take our services and enjoy the best quality of milk and dairy products .
    """

    message = f"Subject: {subject}\n\n{body}"

    server =  smtplib.SMTP("smtp.gmail.com",587)

    server.starttls()
    
    server.login(sender_email,sender_password)
    
    server.sendmail(sender_email, receiver_email, message)

    server.quit()


    