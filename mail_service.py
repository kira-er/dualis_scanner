import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser

def create_grades_table(grades):
    grades_table = "<table> <thead> <tr> <th>Name</th> <th>Note</th> <th>Modul</th> <th>Semester</th> </tr> </thead> <tbody>"
    for grade in grades:
        grades_table += "<tr> <td>" + grade["Name"] + "</td> <td>" + grade["Note"] + "</td> <td>" + grade["Modul"] + "</td> <td>" + grade["Semester"] + "</td> </tr>"

    grades_table += "</tbody> </table>"
    return grades_table

def send_update_mail(receiver_mail, grades):
    config = configparser.ConfigParser()
    config.read("config_mail.ini", encoding="utf8")

    message = MIMEMultipart("alternative")
    message["Subject"] = "Notenupdate"
    message["From"] = config["Mail_Service"]["mail"]
    message["To"] = receiver_mail

    html = "<p>Hey,</p> <p>" + config["Mail_Service"]["update_mailtext"] + "</p>" + create_grades_table(grades)
    part = MIMEText(html, "html")
    message.attach(part)
    create_mail(receiver_mail, message.as_string())

def send_welcome_mail(receiver_mail, grades):
    config = configparser.ConfigParser()
    config.read("config_mail.ini", encoding="utf8")

    message = MIMEMultipart("alternative")
    message["Subject"] = "Dualis Mailservice prints 'Hello_World'"
    message["From"] = config["Mail_Service"]["mail"]
    message["To"] = receiver_mail

    html = "<p>Hey,</p> <p>" + config["Mail_Service"]["welcome_mailtext"] + "</p>" + create_grades_table(grades)
    part = MIMEText(html, "html")
    message.attach(part)
    create_mail(receiver_mail, message.as_string())

def create_mail(receiver_mail, message):
    context = ssl.create_default_context()

    config = configparser.ConfigParser()
    config.read("config_mail.ini", encoding="utf8")

    with smtplib.SMTP_SSL("securesmtp.t-online.de", 465, context=context) as server:
        server.login(config["Mail_Service"]["mail"], config["Mail_Service"]["password"])
        server.sendmail(config["Mail_Service"]["mail"], receiver_mail, message)