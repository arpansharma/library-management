from celery import Celery
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
	print ("Requset Type : " + mail_type)
	if mail_type == 'Issue':
		print ("inside if")
		subject = 'Issue Information'
		content = Content("text/plain",
						  "Dear " + borrower_name + ", you have been issued a book titled "
						  + book_title + " on " + issue_date + ". Please return it before "
						  + due_date + " to avoid any fines. Happy Reading !"
				)
	elif mail_type == 'Return':
		subject = 'Return Information'
		fine_message = ''
		if fine_amount is 0:
			fine_message = '. You have no fine to pay. Happy Reading !'
		else:
			fine_message = '. You have to pay a fine of Rs. ' + str(fine_amount)

		content = Content(
						"text/plain",
						'Dear ' + borrower_name + ', a book titled '
						+ book_title + ' was issued to you on ' + issue_date
						+ ' which was due for return on ' + due_date
						+ '. Your date of return is ' + actual_return_date
						+ fine_message
				)
	# else:
	# 	subject = 'Reminder'
	# 	content = Content(
	# 					"text/plain",
	# 					'Dear ' + borrower_name + ', a book titled '
	# 					+ book_title + ' was issued to you on ' + issue_date
	# 					+ ' which is due for return on ' + due_date
	# 					+ '. Please return it on time to avoid any fine. Happy Reading !'
	# 			)

	mail = Mail(from_email, subject, to_email, content)
	response = sg.client.mail.send.post(request_body=mail.get())

	# print(response.status_code) //202
	# print(response.body)
	# print(response.headers)

