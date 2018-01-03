from django import forms
from userapp.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['pic']
