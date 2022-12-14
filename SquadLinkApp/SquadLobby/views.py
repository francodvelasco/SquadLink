from django.shortcuts import render, redirect
from django.views import View
from UserProfile.models import SquadLinkUserModel
from .models import SquadLinkLobby

from django.contrib.auth.models import User


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
            return redirect('UserProfile:sign-in')

    def post(self, request):
        lobby_create_form = LobbyCreateForm(request.POST, request.FILES)

        if not request.user.is_authenticated:
            return redirect('UserProfile:sign-in')
        elif lobby_create_form.is_valid():
            user = SquadLinkUserModel.objects.get(
                user=request.user)
            lobby_model = SquadLinkLobby.custom_manager.create(
                creator=user, form=lobby_create_form)
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
            page_contents['form'] = LobbyAddMembersForm()

        page_contents['lobby'] = SquadLinkLobby.custom_manager.get(pk=pk)

        # print(page_contents['lobby'].squad_members)
        return render(request, 'squad_page.html', page_contents)

    def post(self, request, pk):
        if request.user.is_authenticated:
            lobby = SquadLinkLobby.custom_manager.get(pk=pk)
            current_user_model = SquadLinkUserModel.objects.get(
                user=request.user)

            # form = LobbyAddMembersForm(request.POST)

            if current_user_model == lobby.creator:
                username_search = request.POST['username']
                user_found = User.objects.get(username=username_search)
                print("I am the owner: ", user_found.id)
                user_add_found = SquadLinkUserModel.objects.get(
                    id=user_found.id-2)

                # print("Being added:", user_add_found.user.id,
                #       user_add_found.user.username, " - user_add", user_add_found.id)
                # print("creator:", lobby.creator.user.id,
                #       lobby.creator.user.username, "- user_add", lobby.creator.id)

                if (user_add_found != lobby.creator):
                    lobby.squad_members.add(user_add_found)
            else:
                user_add_found = current_user_model
                print("I am not the owner: ", user_add_found.id)
                lobby.squad_members.add(user_add_found)

            if user_add_found:
                print(user_add_found.id)
                # print(SquadLinkUserModel.objects.get(id=user_add.id).pk-2)

                lobby.save()

                return self.get(request, pk)
            else:
                page_contents = dict()

                if request.user.is_authenticated:
                    page_contents['user'] = request.user
                    page_contents['user_add'] = SquadLinkUserModel.objects.get(
                        user=request.user)

                page_contents['lobby'] = SquadLinkLobby.objects.get(pk=pk)
                page_contents['no_user_found'] = True

                return render(request, 'squad_page.html', page_contents)
        else:
            return redirect('UserProfile:sign-in')


class LobbyListView(View):
    def get(self, request):
        page_contents = dict()

        if request.user.is_authenticated:
            page_contents['user'] = request.user
            page_contents['user_add'] = SquadLinkUserModel.objects.get(
                user=request.user)

        page_contents['lobbies'] = SquadLinkLobby.custom_manager.all()

        return render(request, 'lobby_list.html', page_contents)


class LobbyEditView(View):
    def get(self, request, pk):
        page_contents = dict()

        if request.user.is_authenticated:
            page_contents['user'] = request.user
            page_contents['user_add'] = SquadLinkUserModel.objects.get(
                user=request.user)
        else:
            return redirect('UserProfile:sign-in')

        lobby = SquadLinkLobby.custom_manager.get(pk=pk)

        # Only the lobby creator can edit the lobby
        # Future iteration: query parameter to show error
        if request.user != lobby.creator.user:
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
            'platforms': list(map(lambda name: platform_dict_reverse[name.strip()], lobby.platforms.split(','))),
            'game': game_dict_reverse[lobby.game],
            'region': region_dict_reverse[lobby.region],
            'rank_lower_bound': lobby.rank_lower_bound,
            'rank_higher_bound': lobby.rank_higher_bound,
            'languages': list(map(lambda name: lang_dict_reverse[name.strip()], lobby.languages.split(','))),
            'squad_size': lobby.squad_size
        }

        page_contents['form'] = LobbyCreateForm(
            request.POST or None, request.FILES or None, initial=lobby_dict)
        return render(request, 'edit_squad.html', page_contents)

    def post(self, request, pk):
        form = LobbyCreateForm(request.POST, request.FILES)
        lobby_model = SquadLinkLobby.custom_manager.get(pk=pk)

        # print(request.POST['game'])
        lobby_model.update_from_form(form)

        return redirect('SquadLobby:lobby-details', pk=pk)
