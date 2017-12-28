from django.urls import path

from evaluationapp.views import EvaluationBase,get_evaluation_from_my_follow

urlpatterns = [
    path('base/', EvaluationBase.as_view()),
    path('get_evaluation_from_my_follow/', get_evaluation_from_my_follow),
]
