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
        page_contents['user'] = request.user

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
            user_platforms = ','.join(
                user_add_creation_form.cleaned_data.get('user_platforms'))
            user_game = user_add_creation_form.cleaned_data.get('user_game')
            rank = user_add_creation_form.cleaned_data.get('rank')

            sl_user_model = SquadLinkUserModel.objects.create(
                user=user,
                profile_image=profile_image,
                platforms=user_platforms,
                game=user_game,
                rank=rank
            )

            sl_user_model.save()

            username = user_creation_form.cleaned_data.get('username')
            password = user_creation_form.cleaned_data.get('password1')

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            print(
                f"Somethings is not valid | base: {user_creation_form.is_valid()}, {user_creation_form.errors} | add: {user_add_creation_form.is_valid()}, {user_add_creation_form.errors}")
            print(f"Base: {user_creation_form.cleaned_data}")
            print(f"Add: {user_add_creation_form.cleaned_data}")
            page_contents = dict()
            page_contents['user_forms'] = user_creation_form
            page_contents['user_add_form'] = user_add_creation_form

            return render(request, 'signup.html', page_contents)


class SquadLinkUserLogInView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')

        page_contents = dict()
        page_contents['form'] = SquadLinkUserLogInForm(request=request)

        return render(request, 'login.html', page_contents)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/')

        login_form = SquadLinkUserLogInForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect('/')
            else:
                return redirect(SquadLinkUserCreationView.as_view())

        else:
            page_contents = dict()
            page_contents['form'] = login_form

            return render(request, 'login.html', page_contents)


class SquadLinkUserView(View):

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            form = SquadLinkUserUpdateForm(instance=user)
            page_content = dict()
            page_content['form'] = form

            return render(request, 'view_profile.html', page_content)

        else:
            return redirect('UserProfile:sign-in')
