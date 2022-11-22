from audioop import reverse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import F

from .models import SquadLinkUserModel
from .forms import SquadLinkUserLogInForm, SquadLinkUserUpdateForm, UserBaseForm, UserAdditionalForm


class SquadLinkHomeView(View):
    def get(self, request):
        page_contents = dict()

        if request.user.is_authenticated:
            page_contents['user'] = request.user
            page_contents['user_add'] = SquadLinkUserModel.objects.get(
                user=request.user)

        return render(request, 'home.html', page_contents)

# Create your views here.


class SquadLinkUserCreationView(View):
    def get(self, request):
        page_contents = {}
        page_contents['user_forms'] = UserBaseForm()
        page_contents['user_add_form'] = UserAdditionalForm()
        return render(request, 'signup.html', page_contents)

    def post(self, request):
        user_creation_form = UserBaseForm(request.POST)
        user_add_creation_form = UserAdditionalForm(
            request.POST, request.FILES)

        if user_creation_form.is_valid() and user_add_creation_form.is_valid():
            user = user_creation_form.save()

            profile_image = user_add_creation_form.cleaned_data.get(
                'profile_image')
            user_platforms = ', '.join(
                user_add_creation_form.cleaned_data.get('user_platforms'))
            user_game = user_add_creation_form.cleaned_data.get('user_game')
            rank = user_add_creation_form.cleaned_data.get('rank')
            region = user_add_creation_form.cleaned_data.get('region')
            bio = user_add_creation_form.cleaned_data.get('bio')

            sl_user_model = SquadLinkUserModel.objects.create(
                user=user,
                profile_image=profile_image,
                platforms=user_platforms,
                game=user_game,
                rank=rank,
                bio=bio,
                region=region
            )

            sl_user_model.save()

            username = user_creation_form.cleaned_data.get('username')
            password = user_creation_form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            page_contents = dict()
            page_contents['user_forms'] = user_creation_form
            page_contents['user_add_form'] = user_add_creation_form

            return render(request, 'signup.html', page_contents)


class SquadLinkUserEditView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('UserProfile:sign-in')

        page_contents = dict()
        user_add = SquadLinkUserModel.objects.get(
            user=request.user)

        user_details_dict = {
            'region': user_add.region,
            'profile_image': user_add.profile_image,
            'user_platforms': list(map(lambda name: name.strip(), user_add.platforms.split(','))),
            'user_game': user_add.game,
            'rank': user_add.rank,
            'bio': user_add.bio
        }

        page_contents['form'] = UserAdditionalForm(
            request.POST or None, request.FILES or None, initial=user_details_dict)

        return render(request, 'edit_profile.html', page_contents)

    def post(self, request):
        if request.user.is_authenticated:
            form = UserAdditionalForm(request.POST, request.FILES)
            user_add = SquadLinkUserModel.objects.get(user=request.user)

            if form.is_valid():
                profile_image = form.cleaned_data.get('profile_image')
                user_platforms = ', '.join(
                    form.cleaned_data.get('user_platforms'))
                user_game = form.cleaned_data.get('user_game')
                rank = form.cleaned_data.get('rank')
                region = form.cleaned_data.get('region')
                bio = form.cleaned_data.get('bio')

                user_to_update = SquadLinkUserModel.objects.get(
                    user=request.user)
                user_to_update.profile_image = profile_image if profile_image else user_add.profile_image
                user_to_update.platforms = user_platforms if user_platforms else user_add.platforms
                user_to_update.game = user_game if user_game else user_add.game
                user_to_update.rank = rank if rank else user_add.rank
                user_to_update.region = region if region else user_add.region
                user_to_update.bio = bio if bio else user_add.bio

                user_to_update.save()

            return redirect('UserProfile:view-profile')
        else:
            return redirect('UserProfile:sign-in')


class SquadLinkUserLogInView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('UserProfile:view-profile')

        page_contents = dict()
        page_contents['form'] = SquadLinkUserLogInForm()

        return render(request, 'login.html', page_contents)

    def post(self, request):
        login_form = SquadLinkUserLogInForm(data=request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('home')

        page_contents = dict()
        page_contents['form'] = login_form

        return render(request, 'login.html', page_contents)


class SquadLinkUserView(View):
    def get(self, request):
        if request.user.is_authenticated:
            page_contents = dict()
            page_contents['user'] = request.user
            page_contents['user_add'] = SquadLinkUserModel.objects.get(
                user=request.user)

            return render(request, 'view_profile.html', page_contents)
        else:
            return redirect('UserProfile:sign-in')


class SquadLinkExternalUserView(View):
    def get(self, request, username):
        page_contents = dict()

        if request.user.is_authenticated:
            page_contents['user'] = request.user
            page_contents['user_add'] = SquadLinkUserModel.objects.get(
                user=request.user)

        page_contents['username_to_view'] = username
        page_contents['user_to_view'] = SquadLinkUserModel.objects.get(
            user__username=username)
        page_contents['viewing_user_only'] = True

        if page_contents['user_add'] == page_contents['user_to_view']:
            return redirect('UserProfile:view-profile')

        return render(request, 'view_external_user.html', page_contents)


class SquadLinkUserSquadsView(View):
    def get(self, request):
        if request.user.is_authenticated:
            page_contents = dict()
            page_contents['user'] = request.user
            user_add = SquadLinkUserModel.objects.get(
                user=request.user)

            page_contents['user_add'] = user_add
            page_contents['squads'] = user_add.members.all()

            return render(request, 'FILE-NAME.html', page_contents)
        else:
            return redirect('UserProfile:sign-in')


class SquadLinkAddFriendsHandler(View):
    def get(self, request, sender, receiver):
        if not request.user.is_authenticated and sender == receiver:
            return redirect('UserProfile:view-profile')

        user_friending = SquadLinkUserModel.objects.get(id=sender)
        user_to_friend = SquadLinkUserModel.objects.get(id=receiver)

        user_friending.requests_sent.add(user_to_friend)
        user_to_friend.requests_received.add(user_friending)

        return redirect(request.META.get('HTTP_REFERER'))


class SquadLinkConfirmFriendsHandler(View):
    def get(self, request, sender, receiver):
        user_friending = SquadLinkUserModel.objects.get(id=sender)
        user_to_friend = SquadLinkUserModel.objects.get(id=receiver)

        user_to_friend.requests_received.delete(user_friending)
        user_friending.requests_sent.delete(user_to_friend)

        user_to_friend.friends.add(user_friending)
        user_friending.friends.add(user_to_friend)

<<<<<<< HEAD
        return redirect(request.META.get('HTTP_REFERER'))
=======
        return redirect('UserProfile:view-profile')

class SquadLinkRejectRequestHandler(View):
    def get(self, request, sender, receiver):
        user_friending = SquadLinkUserModel.objects.get(id=sender)
        user_to_friend = SquadLinkUserModel.objects.get(id=receiver)

        user_to_friend.requests_received.delete(user_friending)
        user_friending.requests_sent.delete(user_to_friend)
        
        return redirect('UserProfile:view-profile')
>>>>>>> 67517aeb9444f9aa599c54daa49e791e158ff10c
