#!/usr/bin/python
##import automatic_email_bash within the gui.py, then call it
import smtplib, ssl, email,os,socket
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re

def sendEmail():
    smtp_server = "smtp.gmail.com" ##dont touch
    port = 587 ##dont touch
    sender_email = "bicycle.email.bot@gmail.com" ##dont change
    password = "Fjun78797bu" ##password must be manually changed by me
    subject = "Bicycle Application Requested Files..."##can be changed
    body = "Here are the Files you requested..." ##can be changed
    connection = False
    #make an array for multiple receiver emails

    data = []
    regex = re.compile('[@]')
    filepath = 'store.txt'

    with open(filepath) as fp:
        for line in fp:
            data.append(line.strip())
            
    try:
        socket.create_connection(("www.google.com", 80))
        connection = True
    except OSError:
        connection = False
    if (connection):
        i = 0  
        while (i < len(data)):
            if ('@' in data[i]):
                receiver_email = data[i]
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = receiver_email
                message["Subject"] = subject
                message["Bcc"] = receiver_email
                message.attach(MIMEText(body, "plain"))
                i = i + 1
                
            while ('@' not in data[i]):
                attachment = open(data[i], "rb")
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= " + data[i])
                message.attach(part)
                text = message.as_string()
                i = i + 1
                if (i == len(data)):
                     break
                     
            context = ssl.create_default_context() #dont touch
            with smtplib.SMTP(smtp_server, port) as server: #dont touch
                server.starttls(context=context) #dont touch
                server.login(sender_email, password) #dont touch
                #add a for statement or while loop to send multiple emails
                server.sendmail(sender_email, receiver_email, text) ##dont touch
                server.quit()
                
        print("Done!")

try:
    socket.create_connection(("www.google.com", 80))
    connection = True
except OSError:
    connection = False
        
if (os.path.isfile("/store.txt")):
    sendEmail()
    os.remove("/store.txt")
    print("Stored files, successfully sent")
elif (connection == False):
    print ("No internet connection")
else:
    print("No stored files")
    


