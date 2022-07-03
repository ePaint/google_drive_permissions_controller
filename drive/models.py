from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from django.utils import timezone

# Create your models here.
class DriveFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    social_user = models.ForeignKey(SocialAccount, on_delete=models.CASCADE)
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    icon_url = models.CharField(max_length=255, blank=True, null=True)
    created_time = models.DateTimeField(null=True)
    modified_time = models.DateTimeField(null=True)
    public = models.BooleanField(default=True)
    processed_time = models.DateTimeField(null=True)

    def __str__(self):
        return f'{self.id} - {self.name}'

class ActionRecord(models.Model):
    file = models.ForeignKey(DriveFile, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return str(self.date)
