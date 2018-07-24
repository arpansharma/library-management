from celery import Celery
from datetime import datetime
from django.conf import settings
import sendgrid
import os
from sendgrid.helpers.mail import *

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def SendMail(
			mail_type,
			book_title,
			borrower_name,
			borrower_email,
			issue_date,
			due_date,
			actual_return_date,
			fine_amount
):
	# sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
	sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
	from_email = Email("arpan.sharma011@gmail.com")
	to_email = Email(borrower_email)

	issue_date = datetime.strptime(issue_date, "%Y-%m-%dT%H:%M:%S")
	due_date = datetime.strptime(due_date, "%Y-%m-%dT%H:%M:%S")
	actual_return_date = datetime.strptime(actual_return_date, "%Y-%m-%dT%H:%M:%S")
	mail_date_format = "%d %B, %Y at %H:%M"
	print ("Requset Type : " + mail_type)

	if mail_type == 'Issue':
		subject = 'Issue Information'
		content = Content("text/plain",
						  "Dear " + borrower_name + ", you have been issued a book titled "
						  + book_title + " on " 
						  + issue_date.strftime(mail_date_format)
						  + ". Please return it before " 
						  + due_date.strftime(mail_date_format)
						  + " to avoid any fines. Happy Reading !"
				)
	elif mail_type == 'Return':
		subject = 'Return Information'
		fine_message = ''
		if fine_amount is None:
			fine_message = '. You have no fine to pay. Happy Reading !'
		else:
			fine_message = '. You have to pay a fine of Rs. ' + str(fine_amount)
		content = Content(
						"text/plain",
						'Dear ' + borrower_name + ', a book titled '
						+ book_title + ' was issued to you on ' 
						+ issue_date.strftime(mail_date_format)
						+ ' which was due for return on ' 
						+ due_date.strftime(mail_date_format)
						+ '. Your date of return is ' 
						+ actual_return_date.strftime(mail_date_format)
						+ fine_message
				)

	mail = Mail(from_email, subject, to_email, content)
	response = sg.client.mail.send.post(request_body=mail.get())

	# print(response.status_code) //202
	# print(response.body)
	# print(response.headers)

