from django.urls import path

from activityapp.views import ActivityBase

urlpatterns = [
    path('base/', ActivityBase.as_view()),
]