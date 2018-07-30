from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views
from .views import (
	HomePage,
	CustomAuthToken,
	BookViewSet,
	StudentViewSet,
	TeacherViewSet,
	BorrowerViewSet,
	IssueSlipViewSet
)

router = routers.SimpleRouter()
router.register('books', BookViewSet)
router.register('issue', IssueSlipViewSet)
router.register('borrower/students', StudentViewSet)
router.register('borrower/teachers', TeacherViewSet)
router.register('borrower', BorrowerViewSet)
router.register('return', IssueSlipViewSet)
urlpatterns = router.urls

urlpatterns += [
	path('api-token-auth/', CustomAuthToken.as_view()),
	path('', HomePage.index, name='index'),
	# path('api-other/', include('django.contrib.auth.urls')),
]