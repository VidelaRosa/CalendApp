from django.db import models
from django.conf import settings

RANGE_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5)
)


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    avatar = models.ImageField(upload_to='avatar',
                               default='avatar/default.jpg')

    def save(self, *args, **kwargs):
        try:
            this = Account.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.delete()
        except:
            pass
        super(Account, self).save(*args, **kwargs)


class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    importance = models.IntegerField(choices=RANGE_CHOICES)


class Job(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    description = models.TextField()
    importance = models.IntegerField(choices=RANGE_CHOICES)
    progress = models.IntegerField(default=0)


class Meeting(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    person = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    importance = models.IntegerField(choices=RANGE_CHOICES)
