from django.urls import path
from hotspotapp.views import HotSpotBase

urlpatterns = [
    path('base/', HotSpotBase.as_view()),
]
