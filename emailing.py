from dotenv import load_dotenv
import smtplib, ssl
from email import encoders
import os
from email.message import EmailMessage
import imghdr


load_dotenv("global.env")
LOGIN = os.getenv("EMAIL_USERNAME")
PASS = os.getenv("EMAIL_PASS")
HOST = "smtp.gmail.com"
PORT = 587

reciver = LOGIN

def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up!"
    email_message.set_content("Hey, we just saw a new customer!")
    
    # loading image file 
    with open(image_path, "rb") as file:
        content = file.read()
    
    email_message.add_attachment(content, maintype="image",
                                 subtype=imghdr.what(None, content))
    
    
    
    gmail = smtplib.SMTP(HOST, PORT)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(LOGIN, PASS)
    gmail.sendmail(LOGIN, reciver, email_message.as_string())
    gmail.quit()

        
    
    print("Email was send")
    
    
    
    
if __name__=="__main__":
    send_email(image_path="images\image1.png")