from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import IssueSlip
from .tasks import SendMail

@receiver(post_save, sender=IssueSlip)
def MailSignal(sender, created, instance, **kwargs):
	if created:
		mail_type = 'Issue'		
	else:
		mail_type = 'Return'

	SendMail.delay(
				   mail_type=mail_type,
				   book_title=instance.book.title,
				   borrower_name=instance.borrower.name,
				   borrower_email=instance.borrower.email,
				   issue_date=instance.issue_date,
				   due_date=instance.due_date,
				   actual_return_date = instance.actual_return_date,
				   fine_amount=instance.fine_amount					
	)


