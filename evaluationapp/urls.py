from django.urls import path

from evaluationapp.views import EvaluationBase

urlpatterns = [
    path('base/', EvaluationBase.as_view()),
]
