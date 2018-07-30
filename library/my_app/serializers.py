from datetime import datetime, timedelta
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

	
	def create(self, validated_data, *args, **kwargs):
		book_object = validated_data['book']
		borrower_object = validated_data['borrower']
		if book_object.is_available is True:
			if borrower_object.borrower_type is 'S' and borrower_object.issue_count < 2:
				book_object.is_available = False
				borrower_object.issue_count += 1
				book_object.save()
				borrower_object.save()
				validated_data['issue_date'] = datetime.now().replace(second=0, microsecond=0)
				validated_data['due_date'] = validated_data['issue_date'] + timedelta(minutes=7)				
				return IssueSlip.objects.create(**validated_data)

			elif borrower_object.borrower_type is 'T' and borrower_object.issue_count < 4:
				book_object.is_available = False
				borrower_object.issue_count += 1
				book_object.save()
				borrower_object.save()
				validated_data['issue_date'] = datetime.now().replace(second=0, microsecond=0)
				validated_data['due_date'] = validated_data['issue_date'] + timedelta(minutes=14)				
				return IssueSlip.objects.create(**validated_data)

			else:
				raise serializers.ValidationError({'message':'Sorry! Max issue count reached'})				
		else:
			raise serializers.ValidationError({'message':'Sorry! The book is not available'})