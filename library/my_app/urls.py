from django.contrib import admin
from django.urls import path
from rest_framework import routers

from .views import BookViewSet, StudentViewSet, TeacherViewSet, BorrowerViewSet, IssueSlipViewSet

router = routers.SimpleRouter()
router.register('books', BookViewSet)
router.register('issue', IssueSlipViewSet)
router.register('login', BookViewSet)
router.register('borrower/students', StudentViewSet)
router.register('borrower/teachers', TeacherViewSet)
router.register('borrower', BorrowerViewSet)
urlpatterns = router.urls

# urlpatterns = [
#   path('books/', BookViewSet.as_view({'get': 'list'})),
# 	path('students/', StudentViewSet.as_view({'get': 'retrieve'})),
# 	path('teachers/', TeacherViewSet.as_view({'get': 'retrieve'})),
# ]