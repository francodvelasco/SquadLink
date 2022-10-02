from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import SquadLinkApp.settings as settings
import os

def profile_image_location(request, filename):
    return os.path.join('uploads', 'profile_images', filename)

class SquadLinkUserModel(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    profile_image = models.ImageField(upload_to=profile_image_location, null=True, blank=True)
    friends = models.ForeignKey(settings.AUTH_USER_MODEL)
    pending_requests = models.ForeignKey(settings.USER_AUTH_MODEL)
    platforms = models.CharField()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        SquadLinkUserModel.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.squadlinkusermodel.save()

# 
# class SquadLinkUser(AbstractUser):
   # username = models.CharField(max_length=64, blank=True, null=True, unique=True)
    #profile_image = models.ImageField(upload_to=profile_image_location, null=True, blank=True)
    

   # def __str__(self):
    #    return self.username