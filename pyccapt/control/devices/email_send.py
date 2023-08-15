import datetime
import smtplib
import ssl


def send_email(email, subject, message):
	"""
	This function sends an email notification via the SMTP server.

	Args:
		email (str): Recipient's email address.
		subject (str): Subject of the email.
		message (str): Main body of the email.

	Returns:
		None
	"""
	port = 465  # For SSL
	smtp_server = "smtp.gmail.com"
	sender_email = "oxcart.ap@gmail.com"
	date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

	with open('./files/email_pass.txt') as f:  # Open file with email password
		password = str(f.readline().strip())
	receiver_email = email

	msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (sender_email, email, subject, date, message)

	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, msg)
