from audioop import reverse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

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

            if form.is_valid():
                profile_image = form.cleaned_data.get('profile_image')
                user_platforms = ', '.join(
                    form.cleaned_data.get('user_platforms'))
                user_game = form.cleaned_data.get('user_game')
                rank = form.cleaned_data.get('rank')
                region = form.cleaned_data.get('region')
                bio = form.cleaned_data.get('bio')

                sl_user_model = SquadLinkUserModel.objects.create(
                    user=request.user,
                    profile_image=profile_image,
                    platforms=user_platforms,
                    game=user_game,
                    rank=rank,
                    bio=bio,
                    region=region
                )

                sl_user_model.save()

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
