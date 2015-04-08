"""
Copyright 2015 Victor de la Rosa Sanchez
This file is part of CalendApp.

    CalendApp is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License.

    CalendApp is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with CalendApp.  If not, see <http://www.gnu.org/licenses/>.
"""
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
