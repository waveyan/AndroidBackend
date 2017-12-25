from django import forms
from evaluationapp.models import Evaluation


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['rate', 'feeling', 'pic1', 'pic2', 'pic3', 'price']
