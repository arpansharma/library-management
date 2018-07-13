from rest_framework import serializers
from .models import Book, Borrower, IssueSlip


class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = [
			'id',
			'title',
			'author',
		]

class BookDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = '__all__'
		# exclude = ('is_active',)

class BorrowerSerializer(serializers.ModelSerializer):	
	class Meta:
		model = Borrower
		fields = [
			'id',
			'name',
			'issue_count',
		]

class BorrowerDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Borrower
		exclude = ('borrower_type', 'is_active',)

class IssueSlipSerializer(serializers.ModelSerializer):
	class Meta:
		model = IssueSlip
		fields = '__all__'