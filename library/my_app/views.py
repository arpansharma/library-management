from datetime import datetime, timedelta
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Book, Borrower, IssueSlip
from .tasks import SendMail
from .serializers import (
    BookSerializer,
    BookDetailSerializer,
    BorrowerSerializer,
    BorrowerDetailSerializer,
    IssueSlipSerializer
)


# def ObjectInactive(self, request, pk):
#     object = self.get_object()
#     object.is_active = False
#     object.save()
#     return Response("{'message':'Deleted'}",status=status.HTTP_200_OK)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        # import ipdb; ipdb.set_trace()        
        if hasattr(self, 'action') and self.action == 'list':   
            return BookSerializer

        elif hasattr(self, 'action') and self.action == 'retrieve':
            return BookDetailSerializer

        return BookDetailSerializer
        
    def destroy(self, request, pk):
        book = self.get_object()
        book.is_active = False
        book.save()
        return Response("{'message':'Deleted'}",status=status.HTTP_200_OK)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.filter(borrower_type__iexact='S')

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'list':   
            return BorrowerSerializer

        elif hasattr(self, 'action') and self.action == 'retrieve':
            return BorrowerDetailSerializer

        return BorrowerDetailSerializer

    def destroy(self, request, pk):
        student = self.get_object()
        student.is_active = False
        student.save()
        return Response("{'message':'Deleted'}",status=status.HTTP_200_OK)

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.filter(borrower_type__iexact='T')

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'list':   
            return BorrowerSerializer

        elif hasattr(self, 'action') and self.action == 'retrieve':
            return BorrowerDetailSerializer

        return BorrowerDetailSerializer

    def destroy(self, request, pk):
        teacher = self.get_object()
        teacher.is_active = False
        teacher.save()
        return Response("{'message':'Deleted'}",status=status.HTTP_200_OK)

class BorrowerViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.all()
    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'list':
            return BorrowerSerializer

        elif hasattr(self, 'action') and self.action == 'retrieve':
            return BorrowerDetailSerializer

        return BorrowerDetailSerializer

class IssueSlipViewSet(viewsets.ModelViewSet):
    queryset = IssueSlip.objects.all()
    serializer_class = IssueSlipSerializer
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'msg': 'The Book has been issued'}, status=status.HTTP_201_CREATED)
    
    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        issue_object = IssueSlip.objects.get(id=kwargs['pk'])
        book_object = Book.objects.get(id=issue_object.book_id)
        borrower_object = Borrower.objects.get(id=issue_object.borrower_id)
        book_object.is_available = True
        borrower_object.issue_count -= 1
        book_object.save()
        borrower_object.save()
        issue_object.actual_return_date = datetime.now()
        issue_object.save()
        if issue_object.due_date >= issue_object.actual_return_date:
            SendMail.delay(
                mail_type = 'Return',
                book_title = book_object.title,
                borrower_name = borrower_object.name,
                borrower_email = borrower_object.email,
                issue_date = issue_object.issue_date,
                due_date = issue_object.due_date,
                actual_return_date = issue_object.actual_return_date,
                fine_amount = 0
            )
            return Response({'msg': 'You have no fine to pay'}, status=status.HTTP_200_OK)
        else:
            elapsed_time = issue_object.actual_return_date - issue_object.due_date
            issue_object.fine_amount = elapsed_time.seconds//60
            SendMail.delay(
                mail_type = 'Return',
                book_title = book_object.title,
                borrower_name = borrower_object.name,
                borrower_email = borrower_object.email,
                issue_date = issue_object.issue_date,
                due_date = issue_object.due_date,
                actual_return_date = issue_object.actual_return_date,
                fine_amount = issue_object.fine_amount
            )
            return Response({'msg': 'You have a fine to pay', 'fine': issue_object.fine_amount}, status=status.HTTP_200_OK)

        issue_object.save()
        self.update(request, *args, **kwargs)

# def list(self, request):
#         pass

# def create(self, request):
#     pass

# def retrieve(self, request, pk=None):
#     pass

# def update(self, request, pk=None):
#     pass

# def partial_update(self, request, pk=None):
#     pass

# def destroy(self, request, pk=None):
#     pass