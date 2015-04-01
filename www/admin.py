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
