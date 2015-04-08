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
# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Account, Event, Job, Meeting


class AccountAdmin(admin.ModelAdmin):
    list_display = (u'id', 'user', 'avatar')
    list_filter = ('user',)
admin.site.register(Account, AccountAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = (
        u'id',
        'user',
        'title',
        'description',
        'date',
        'time',
        'importance',
    )
    list_filter = ('user', 'date')
admin.site.register(Event, EventAdmin)


class JobAdmin(admin.ModelAdmin):
    list_display = (u'id', 'user', 'description', 'importance', 'progress')
    list_filter = ('user',)
admin.site.register(Job, JobAdmin)


class MeetingAdmin(admin.ModelAdmin):
    list_display = (u'id', 'user', 'person', 'date', 'time', 'importance')
    list_filter = ('user', 'date')
admin.site.register(Meeting, MeetingAdmin)
