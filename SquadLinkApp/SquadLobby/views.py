from django.shortcuts import render, redirect
from django.views import View
from UserProfile.models import SquadLinkUserModel
from .models import SquadLinkLobby

from .forms import *
# Create your views here.


class LobbyCreateView(View):
    def get(self, request):
        if request.user.is_authenticated:
            page_contents = dict()

            page_contents['user'] = request.user
            page_contents['user_add'] = SquadLinkUserModel.objects.get(
                user=request.user)
            page_contents['form'] = LobbyCreateForm()

            return render(request, 'create_squad.html', page_contents)
        else:
            redirect('UserProfile:sign-in')

    def post(self, request):
        lobby_create_form = LobbyCreateForm(request.POST, request.FILES)

        if not request.user.is_authenticated:
            return redirect('UserProfile:sign-in')
        elif lobby_create_form.is_valid():
            lobby_model = SquadLinkLobby.custom_manager.create(
                user=request.user, form=lobby_create_form)
            lobby_model.save()

            return redirect('SquadLobby:lobby-list')
        else:
            page_contents = dict()

            page_contents['user'] = request.user
            page_contents['user_add'] = SquadLinkUserModel.objects.get(
                user=request.user)
            page_contents['form'] = lobby_create_form

            return render(request, 'create_squad.html', page_contents)


class LobbyDetailsView(View):
    def get(self, request, pk):
        page_contents = dict()

        if request.user.is_authenticated:
            page_contents['user'] = request.user
            page_contents['user_add'] = SquadLinkUserModel.objects.get(
                user=request.user)

        page_contents['lobby'] = SquadLinkLobby.objects.get(pk=pk)

        return render(request, 'FILE-NAME.html', page_contents)


class LobbyListView(View):
    def get(self, request):
        page_contents = dict()

        if request.user.is_authenticated:
            page_contents['user'] = request.user
            page_contents['user_add'] = SquadLinkUserModel.objects.get(
                user=request.user)

        page_contents['lobbies'] = SquadLinkLobby.objects.all()

        return render(request, 'FILE-NAME.html', page_contents)


class LobbyEditView(View):
    def get(self, request, pk):
        page_contents = dict()

        if request.user.is_authenticated:
            page_contents['user'] = request.user
            page_contents['user_add'] = SquadLinkUserModel.objects.get(
                user=request.user)
        else:
            return redirect('UserProfile:sign-in')

        lobby = SquadLinkLobby.objects.get(pk=pk)

        # Only the lobby creator can edit the lobby
        # Future iteration: query parameter to show error
        if request.user != lobby.user:
            return redirect('SquadLobby:lobby-list')

        platform_dict_reverse = dict((name, code)
                                     for code, name in LobbyCreateForm.PLATFORMS)
        game_dict_reverse = dict((name, code)
                                 for code, name in LobbyCreateForm.GAMES)
        region_dict_reverse = dict((name, code)
                                   for code, name in LobbyCreateForm.REGIONS)
        lang_dict_reverse = dict((name, code)
                                 for code, name in LobbyCreateForm.LANGUAGES)

        lobby_dict = {
            'squad_name': lobby.squad_name,
            'description': lobby.description,
            'photo': lobby.photo,
            'platforms': list(map(lambda name: platform_dict_reverse[name], lobby.platforms.split(','))),
            'game': game_dict_reverse[lobby.game],
            'region': region_dict_reverse[lobby.region],
            'rank_lower_bound': lobby.rank_lower_bound,
            'rank_higher_bound': lobby.rank_higher_bound,
            'languages': list(map(lambda name: lang_dict_reverse[name], lobby.languages.split(','))),
            'squad_size': lobby.squad_size
        }

        page_contents['form'] = LobbyCreateForm(
            request.POST or None, request.FILES or None, initial=lobby_dict)

        return render(request, 'FILE-NAME.html', page_contents)

    def post(self, request, pk):
        form = LobbyCreateForm(request.POST, request.FILES)
        lobby_model = SquadLinkLobby.objects.get(pk=pk)

        lobby_model.update_from_form(form)

        return redirect('SquadLobby:lobby-details', pk=pk)
