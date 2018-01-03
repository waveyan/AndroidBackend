from django.urls import path
from hotspotapp.views import HotSpotBase, create_index, RouteBase

urlpatterns = [
    path('base/', HotSpotBase.as_view()),
    path('create_index/', create_index),
    path('route/', RouteBase.as_view()),
]
