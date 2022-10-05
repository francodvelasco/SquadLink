from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UserBaseForm(UserCreationForm):
    email = None
    first_name = None

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, request=None, *args, **kwargs) -> None:
        super(UserCreationForm, self).__init__(request, *args, **kwargs)
        self.fields['username'].label = 'SquadLink Username'
        self.fields['password1'].label = 'Enter Password'
        self.fields['password2'].label = 'Confirm Password'

        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None

    def clean_username(self):
        username = self.cleaned_data.get('username')
        users = User.objects.filter(username=username)

        if users:
            raise forms.ValidationError("Username already exists")
        else:
            return username


class UserAdditionalForm(forms.Form):
    PLATFORMS = (
        ('PC', 'PC'),
        ('PS', 'PlayStation'),
        ('XB', 'Xbox'),
        ('NS', 'Nintendo Switch')
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

    profile_image = forms.ImageField()
    user_platforms = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices=PLATFORMS)
    user_game = forms.ChoiceField(choices=GAMES, initial='VALO')
    rank = forms.CharField(max_length=100)


class SquadLinkUserLogInForm(AuthenticationForm):
    def __init__(self, request, *args, **kwargs) -> None:
        super(SquadLinkUserLogInForm, self).__init__(request, *args, **kwargs)
