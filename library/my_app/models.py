from django.db import models

class Book(models.Model):
	title = models.CharField(max_length=250)
	author = models.CharField(max_length=250)
	pages = models.IntegerField()
	publication = models.CharField(max_length=250)
	year_of_pub = models.IntegerField()
	is_active = models.BooleanField()
	is_available = models.BooleanField()

class Borrower(models.Model):
	BORROWER_TYPES = (
		('S', 'Student'),
		('T', 'Teacher'),
	)
	borrower_type = models.CharField(max_length=1, choices=BORROWER_TYPES) 
	name = models.CharField(max_length=250)
	email = models.EmailField()
	phone = models.IntegerField()
	issue_count = models.IntegerField()
	is_active = models.BooleanField()

class IssueSlip(models.Model):
	borrower_id = models.ForeignKey(Borrower, on_delete=models.CASCADE)
	book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
	issue_date = models.DateField(auto_now_add=True)
	due_date = models.DateField(blank=True)
	actual_return_date = models.DateField(blank=True, null=True)
