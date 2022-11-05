from django import forms
from django.core.exceptions import ValidationError


def valid_squad_member_count(value):
    if value < 1:
        raise ValidationError(
            'Not enough Squad members. Minimum of 3 (including you, the creator) required.')


class LobbyCreateForm(forms.Form):
    PLATFORMS = (
        ('PC', 'PC'),
        ('PS', 'PlayStation'),
        ('XB', 'Xbox'),
        ('NS', 'Nintendo Switch'),
        ('MB', 'Mobile')
    )

    GAMES = (
        ('VALO', 'Valorant'),
        ('APEX', 'Apex Legends'),
        ('DOTA', 'DOTA 2'),
        ('LEAG', 'League of Legends'),
        ('MLBB', 'Mobile Legends'),
        ('POKE', 'Pokémon Unite'),
        ('CSGO', 'Counter-Strike: Global Offensive (CS:GO)'),
        ('WOFW', 'World of Warcraft')
    )

    REGIONS = (
        ('SG', 'Singapore'),
        ('JP', 'Tokyo'),
        ('HK', 'Hong Kong'),
        ('KR', 'Seoul'),
        ('IN', 'Mumbai'),
        ('AU', 'Sydney')
    )

    LANGUAGES = (
        ('ENG', 'English'),
        ('FIL', 'Filipino'),
        ('JAP', 'Japanese'),
        ('KOR', 'Korean'),
        ('CHN', 'Chinese (Mandarin)'),
        ('ESP', 'Spanish'),
        ('FRA', 'French')
    )

    squad_name = forms.CharField(max_length=128)
    description = forms.CharField(max_length=280)
    photo = forms.ImageField()

    platforms = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=PLATFORMS
    )

    game = forms.ChoiceField(
        choices=GAMES,
        initial='VALO'
    )

    region = forms.ChoiceField(
        choices=REGIONS,
        initial='SG'
    )

    rank_lower_bound = forms.CharField(max_length=100)
    rank_upper_bound = forms.CharField(max_length=100)

    languages = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=LANGUAGES
    )

    squad_size = forms.IntegerField(min_value=2)


class LobbyAddMembersForm(forms.Form):
    username = forms.CharField(max_length=150)


class LobbySearchForm(forms.Form):
    search_term = forms.CharField(max_length=128, required=False)
    match_profile = forms.BooleanField(required=False)

    platforms = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=LobbyCreateForm.PLATFORMS, required=False
    )

    games = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=LobbyCreateForm.GAMES, required=False
    )

    region = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=LobbyCreateForm.REGIONS, required=False
    )

    rank_lower_bound = forms.CharField(max_length=100, required=False)
    rank_upper_bound = forms.CharField(max_length=100, required=False)

    languages = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=LobbyCreateForm.LANGUAGES, required=False
    )

    min_squad_size = forms.IntegerField(min_value=2, required=False)
    max_squad_size = forms.IntegerField(min_value=2, required=False)
