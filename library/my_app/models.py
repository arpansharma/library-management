from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Book(models.Model):
	title = models.CharField(max_length=250)
	author = models.CharField(max_length=250)
	pages = models.IntegerField()
	publication = models.CharField(max_length=250)
	year_of_pub = models.IntegerField()
	is_active = models.BooleanField()
	is_available = models.BooleanField()

	class Meta:
		permissions = (
			('read_book', 'Can Read Book'),
		)

class Borrower(models.Model):
	BORROWER_TYPES = (
		('S', 'Student'),
		('T', 'Teacher'),
	)
	# user = models.OneToOneField(User, on_delete=models.CASCADE)
	borrower_type = models.CharField(max_length=1, choices=BORROWER_TYPES) 
	name = models.CharField(max_length=250)
	email = models.EmailField()
	phone = models.IntegerField()
	issue_count = models.IntegerField()
	is_active = models.BooleanField()

	class Meta:
		permissions = (
			('read_borrower', 'Can Read Borrower'),
		)

class IssueSlip(models.Model):
	borrower = models.ForeignKey(Borrower, blank=True, on_delete=models.CASCADE)
	book = models.ForeignKey(Book, blank=True, on_delete=models.CASCADE)
	issue_date = models.DateTimeField(blank=True)
	due_date = models.DateTimeField(blank=True)
	actual_return_date = models.DateTimeField(blank=True, null=True, default=None)
	fine_amount = models.IntegerField(blank=True, null=True, default=None)
	reminder_count = models.IntegerField(blank=True, null=True, default=None)

	# def save(self, *args, **kwargs):
	# 	self.issue_date = datetime.now()
	# 	self.due_date = self.issue_date + timedelta(minutes=7)
	# 	self.book.is_available = False
	# 	self.borrower.issue_count += 1
	# 	self.book.save()
	# 	self.borrower.save()
	# 	super(IssueSlip, self).save(*args, **kwargs)