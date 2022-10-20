from re import A
from django.db import models
from UserProfile.models import SquadLinkUserModel
from .forms import LobbyCreateForm
import os

def lobby_image_location(request, filename):
    return os.path.join('uploads', 'lobby_images', filename)

class SquadLinkLobbyManager(models.Manager):
    def create(self, *args, **kwargs):
        user = kwargs['user'] if 'user' in kwargs and isinstance(kwargs['user'], SquadLinkUserModel) else None
        form = kwargs['form'] if 'form' in kwargs and isinstance(kwargs['form'], LobbyCreateForm) else None

        if user and form:
            kwargs['creator'] = user
            kwargs['squad_name'] = form.cleaned_data.get('squad_name')
            kwargs['description'] = form.cleaned_data.get('description')
            kwargs['photo'] = form.cleaned_data.get('photo')

            platform_dict = dict(LobbyCreateForm.PLATFORMS)
            kwargs['platforms'] = ', '.join(map(lambda short: platform_dict[short], form.cleaned_data.get('platforms')))

            game_dict = dict(LobbyCreateForm.GAMES)
            kwargs['game'] = game_dict[form.cleaned_data.get('game')]

            region_dict = dict(LobbyCreateForm.REGIONS)
            kwargs['region'] = region_dict[form.cleaned_data.get('region')]

            kwargs['rank_lower_bound'] = form.cleaned_data.get('rank_lower_bound')
            kwargs['rank_upper_bound'] = form.cleaned_data.get('rank_upper_bound')

            lang_dict = dict(LobbyCreateForm.LANGUAGES)
            kwargs['languages'] = ', '.join(map(lambda code: lang_dict[code], form.cleaned_data.get('languages')))

            kwargs['squad_size'] = form.cleaned_data.get('squad_size')

        return super(SquadLinkLobbyManager, self).create(*args, **kwargs)


# Create your models here.
class SquadLinkLobby(models.Model):
    creator = models.ForeignKey(SquadLinkUserModel, on_delete=models.CASCADE)
    squad_name = models.CharField(max_length=128)

    squad_members = models.ManyToManyField(SquadLinkUserModel, related_name='members', blank=True)
    description = models.CharField(max_length=280)
    photo = models.ImageField(upload_to=lobby_image_location, null=True, blank=True)
    platforms = models.CharField(max_length=100, blank=True)
    game = models.CharField(max_length=100, blank=True, default='')
    region = models.CharField(max_length=100, blank=True)

    rank_lower_bound = models.CharField(max_length=100)
    rank_higher_bound = models.CharField(max_length=100)

    languages = models.CharField(max_length=300)
    squad_size = models.IntegerField()

    custom_manager = SquadLinkLobbyManager()

    def update_from_form(self, form: LobbyCreateForm):
        if form and isinstance(form, LobbyCreateForm):
            form_content = form.cleaned_data

            platform_dict = dict(LobbyCreateForm.PLATFORMS)
            form_content['platforms'] = ', '.join(map(lambda short: platform_dict[short], form_content.get('platforms')))

            game_dict = dict(LobbyCreateForm.GAMES)
            form_content['game'] = game_dict[form_content.get('game')]

            region_dict = dict(LobbyCreateForm.REGIONS)
            form_content['region'] = region_dict[form_content.get('region')]

            lang_dict = dict(LobbyCreateForm.LANGUAGES)
            form_content['languages'] = ', '.join(map(lambda code: lang_dict[code], form_content.get('languages')))

            for key, value in form_content.items():
                setattr(self, key, value)
            
            self.save()