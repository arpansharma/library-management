from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Borrower, IssueSlip
from .serializers import (
    BookSerializer,
    BookDetailSerializer,
    BorrowerSerializer,
    BorrowerDetailSerializer,
    IssueSlipSerializer
)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    # serializer_class = BookDetailSerializer

    def get_serializer_class(self):
        # import ipdb; ipdb.set_trace()        
        if hasattr(self, 'action') and self.action == 'list':   
            return BookSerializer

        if hasattr(self, 'action') and self.action == 'retrieve':
            return BookDetailSerializer
        
    def destroy(self, request, pk):
        book = self.get_object()
        book.is_active = False
        book.save()
        return Response("{'message':'Deleted'}",status=status.HTTP_200_OK)

    # return BookDetailSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.filter(borrower_type__iexact='S')

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'list':   
            return BorrowerSerializer

        if hasattr(self, 'action') and self.action == 'retrieve':
            return BorrowerDetailSerializer

    def destroy(self, request, pk):
        student = self.get_object()
        student.is_active = False
        student.save()
        return Response(['Deleted'],status=status.HTTP_200_OK)

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.filter(borrower_type__iexact='T')

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'list':   
            return BorrowerSerializer

        if hasattr(self, 'action') and self.action == 'retrieve':
            return BorrowerDetailSerializer

    def destroy(self, request, pk):
        teacher = self.get_object()
        teacher.is_active = False
        teacher.save()
        return Response(['Deleted'],status=status.HTTP_200_OK)

class BorrowerViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.all()
    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'list':
            return BorrowerSerializer

        if hasattr(self, 'action') and self.action == 'retrieve':
            return BorrowerDetailSerializer

    # def list

class IssueSlipViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = IssueSlipSerializer














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