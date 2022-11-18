from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import SquadLinkApp.settings as settings
import os

def profile_image_location(request, filename):
    return os.path.join('uploads', 'profile_images', filename)

class SquadLinkUserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True, null=True)
    requests_sent = models.ManyToManyField('self', blank=True, null=True)
    requests_received = models.ManyToManyField('self', blank=True, null=True)
    profile_image = models.ImageField(upload_to="upload/", null=True, blank=True)
    platforms = models.CharField(max_length=100, blank=True)
    game = models.CharField(max_length=100, blank=True, default='')
    rank = models.CharField(max_length=100, blank=True, default='')
    bio = models.CharField(max_length=280, blank=True, default='')
    region = models.CharField(max_length=100, blank=True)
