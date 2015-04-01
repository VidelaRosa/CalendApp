from django import forms
from django.contrib.auth import get_user_model
from www.models import *

User = get_user_model()


class UserForm(forms.ModelForm):
    class Meta:
        fields = ["username", "first_name", "last_name", "email", "password"]
        model = User


class EventForm(forms.ModelForm):
    class Meta:
        fields = ["title", "description", "date", "time", "importance"]
        model = Event


class JobForm(forms.ModelForm):
    class Meta:
        fields = ["description", "importance", "progress"]
        model = Job


class MeetingForm(forms.ModelForm):
    class Meta:
        fields = ["person", "date", "time", "importance"]
        model = Meeting
