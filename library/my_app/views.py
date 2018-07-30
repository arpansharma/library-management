from datetime import datetime, timedelta
from rest_framework import viewsets, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from .models import Book, Borrower, IssueSlip
from .permissions import (
    ReadBookPermission,
    ReadUpdateStudentPermission,
    ReadUpdateTeacherPermission
)
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


class CustomAuthToken(ObtainAuthToken):


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class BookViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (ReadBookPermission,)
    queryset = Book.objects.all()
       
    def get_serializer_class(self):

        if hasattr(self, 'action') and self.action == 'list':               
            return BookSerializer

        elif hasattr(self, 'action') and self.action == 'retrieve':
            return BookDetailSerializer
        
        return BookDetailSerializer
        
    def destroy(self, request, pk):
        book = self.get_object()
        book.is_active = False
        book.is_available = False
        book.save()
        return Response("{'message':'Deleted'}",status=status.HTTP_200_OK)

class StudentViewSet(viewsets.ModelViewSet):

    queryset = Borrower.objects.filter(borrower_type__iexact='S')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (ReadUpdateStudentPermission,)

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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (ReadUpdateTeacherPermission,)

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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser,)

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'list':
            return BorrowerSerializer

        elif hasattr(self, 'action') and self.action == 'retrieve':
            return BorrowerDetailSerializer

        return BorrowerDetailSerializer

class IssueSlipViewSet(viewsets.ModelViewSet):

    queryset = IssueSlip.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminUser),
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
        actual_return_date = datetime.now().replace(second=0, microsecond=0)
        if issue_object.due_date >= actual_return_date:    
            request.data['actual_return_date'] = actual_return_date
            self.update(request, *args, **kwargs)            
            return Response({'msg': 'You have no fine to pay'}, status=status.HTTP_200_OK)
        else:
            elapsed_time = actual_return_date - issue_object.due_date
            fine_amount = elapsed_time.seconds//60
            request.data['actual_return_date'] = actual_return_date
            request.data['fine_amount'] = fine_amount            
            self.update(request, *args, **kwargs)
            return Response({'msg': 'You have a fine to pay', 'fine': fine_amount}, status=status.HTTP_200_OK)

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