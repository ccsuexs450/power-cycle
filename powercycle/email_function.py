import smtplib, ssl, email
import socket
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendEmail(receiver_email, password, filename):
    smtp_server = "smtp.gmail.com" ##dont touch
    port = 587 ##dont touch
    subject = "Bicycle Application Requested Files..."##can be changed
    body = "Here are the Files you requested..."
    sender_email = "bicycle.email.bot@gmail.com"
    password = password  ##bicycle.email.bot@gmail.com"
    connection = False
   
    message = MIMEMultipart()
    message["To"] = receiver_email[0]
    message["Subject"] = subject
    message["Bcc"] = receiver_email[0]

    message.attach(MIMEText(body, "plain"))

    #make an array for multiple files
    test = 0
    try:
        socket.create_connection(("www.google.com", 80))
        connection = True
    except OSError:
        connection = False
    if (test == 0):
        ##make a loop for opening all files in the file array
        ##each of these lines is needed to attach the file,
        ##the loop must go through all these lines before repeating
        for i in range(len(filename)):
            attachment = open(filename[i], "rb")
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= " + filename[i])
            message.attach(part)

        text = message.as_string()
        context = ssl.create_default_context() #dont touch
        with smtplib.SMTP(smtp_server, port) as server: #dont touch
            server.starttls(context=context) #dont touch
            while True: # until we login
                try:
                    server.login(sender_email, password)
                except smtplib.SMTPAuthenticationError:
                    print('Login failure: please reenter credential information.')
                    sender_email = input("Enter Email: ")
                    password = input("Enter Password: ")  ##bicycle.email.bot@gmail.com"
                    message["From"] = sender_email
                    continue
                break
                      
            server.sendmail(sender_email, receiver_email, text) ##dont touch
            server.quit() 
            
        print("Done!")
    else:
        print("There is no internet connection, files were safely stored")
        f = open("store.txt","a+")
        f.write(receiver_email[0])
        f.write("\n")
        for i in range(len(filename)):
            f.write(filename[i])
            f.write("\n")
        f.close()


