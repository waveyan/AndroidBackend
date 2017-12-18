from django.urls import path
from userapp.views import UserManager, get_my_follow

urlpatterns = [
    path('base/', UserManager.as_view()),
    path('get_my_follow/', get_my_follow),
]
