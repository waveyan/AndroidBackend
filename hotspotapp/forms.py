from django import forms
from hotspotapp.models import Route


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['title','time','introduce']