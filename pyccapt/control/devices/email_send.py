import datetime
import smtplib
import ssl
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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

	# Create a MIME multipart message
	msg = MIMEMultipart()
	msg['From'] = sender_email
	msg['To'] = email
	msg['Subject'] = subject
	msg['Date'] = date

	# Introduction text
	intro_text = "Dear recipient,\n\n"
	intro_text += "Below is the experiment information:\n\n"

	# Attach the logo image
	logo_path = './files/logo3.png'  # Path to your logo image
	with open(logo_path, 'rb') as f:
		logo_data = f.read()
	logo_image = MIMEImage(logo_data, name='logo.png')
	msg.attach(logo_image)

	# Attach the introduction text
	intro = MIMEText(intro_text + message, 'plain')
	msg.attach(intro)


	# Send the email
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, msg.as_string())
