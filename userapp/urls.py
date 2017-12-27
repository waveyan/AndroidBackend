from django.urls import path
from userapp.views import UserManager, get_my_follow, get_my_favour, get_my_activity

urlpatterns = [
    path('base/', UserManager.as_view()),
    path('get_my_follow/', get_my_follow),
    path('get_my_favour/', get_my_favour),
    path('get_my_activity/', get_my_activity),
]
