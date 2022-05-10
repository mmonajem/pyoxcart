import smtplib, ssl
import datetime

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "oxcart.ap@gmail.com"
# password = "Subkorn1"
date = datetime.datetime.now().strftime( "%d/%m/%Y %H:%M" )


def send_email(email, subject, message):
    """
     This function is responsible to send email notification onto SMTP server.

     Attributes:
        subject: subject of the email which need to be send
        message: Main body of email.

    Return:
        Does not return anything
    """
    with open('../../files/email_pass.txt') as f:
        password = str(f.readlines()[0])
    receiver_email = email

    msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (sender_email, email, subject, date, message)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg)


