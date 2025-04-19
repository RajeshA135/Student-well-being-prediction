from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class StudentInputForm(forms.Form):
    pss_score = forms.IntegerField()
    psqi_score = forms.IntegerField()
    sleep_hours = forms.FloatField()
    activities_hours = forms.FloatField()

class UploadDatasetForm(forms.Form):
    dataset = forms.FileField()