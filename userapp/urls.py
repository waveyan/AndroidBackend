from django.urls import path
from userapp.views import UserManager

urlpatterns = [
    path('base/', UserManager.as_view()),
]
