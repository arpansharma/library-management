from django.core.management import BaseCommand
from my_app.models import Book, Borrower, IssueSlip
from django.conf import settings
import sendgrid
import os
from sendgrid.helpers.mail import *

#The class must be named Command, and subclass BaseCommand
class Command(BaseCommand):
	# Show this when the user types help
	help = "Reminder for return of Books"

	# A command must define handle()
	def handle(self, *args, **options):
		print("About to send mail")
		sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
		from_email = Email("arpan.sharma011@gmail.com")		
		reminder_objects = IssueSlip.objects.filter(actual_return_date = None)
		if reminder_objects:
			for object in reminder_objects:
				book_object = Book.objects.get(id=object.book_id)
				borrower_object = Borrower.objects.get(id=object.borrower_id)
				if object.reminder_count is None:
					object.reminder_count = 0
				else:
					object.reminder_count += 1
				object.save()
				to_email = Email(borrower_object.email)
				subject = 'Reminder'
				content = Content(
								"text/plain",
								'Dear ' + borrower_object.name + ', a book titled '
								+ book_object.title + ' was issued to you on ' + str(object.issue_date)
								+ ' which is due for return on ' + str(object.due_date)
								+ '. Please return it on time to avoid any fine. Happy Reading !'
						)
				mail = Mail(from_email, subject, to_email, content)
				response = sg.client.mail.send.post(request_body=mail.get())
#crontab = MIN HOUR DOM MON DOW CMD