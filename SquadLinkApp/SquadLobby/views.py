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

            form = LobbyAddMembersForm(request.POST)
            # username_search = form.cleaned_data.get('username')
            username_search = request.POST['username']

            # user_to_add = None
            # print('\nHELP US', current_user_model, "sdadas", lobby.creator)
            # if current_user_model == lobby.creator:
            #     user_to_add = SquadLinkUserModel.objects.filter(
            #         user__username=username_search).first()
            # else:
            #     # user_to_add = SquadLinkUserModel.objects.filter(user__username=request.user.username).first()
            #     user_to_add = current_user_model

            if username_search:
                # print('this is THE UISER TO ADD', user_to_add)
                # lobby.squad_members.add(SquadLinkUserModel.objects.filter(
                #     user__username=username_search).first())
                user_add = User.objects.get(username=username_search)
                print()
                print()
                print()
                print(user_add.id)
                print(SquadLinkUserModel.objects.get(
                    id=user_add.id))
                lobby.squad_members.add(SquadLinkUserModel.objects.get(
                    id=user_add.id).pk-2)

                # print("\n", SquadLinkUserModel._meta.fields)
                # print("\n", SquadLinkUserModel._meta.fields[1]._meta.fields)
                # print("\n", SquadLinkUserModel.objects.filter(user=username_search))
                print("LOBBMEMEMMEE", lobby._meta.fields)
                print("LOBBMEMEMMEE", lobby.squad_members.all())
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
