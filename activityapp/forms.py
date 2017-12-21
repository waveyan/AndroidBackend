from django import forms
from activityapp.models import Activity


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['host_user', 'title', 'subject', 'time', 'type', 'introduction', 'person', 'telephone', 'website',
                  'pic1', 'pic2', 'pic3', 'price']
