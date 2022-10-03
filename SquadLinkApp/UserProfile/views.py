from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import SquadLinkUserLogInForm, UserBaseForm, UserAdditionalForm

# Create your views here.


class SquadLinkUserCreationView(View):
    def get(self, request):
        page_contents = {}
        page_contents['user_forms'] = UserBaseForm()
        page_contents['user_add_form'] = UserAdditionalForm()
        return render(request, 'signup.html', page_contents)

    def post(self, request):
        user_creation_form = UserBaseForm(request.POST)
        user_add_creation_form = UserAdditionalForm(request.POST)

        if user_creation_form.is_valid() and user_add_creation_form.is_valid():
            user = user_creation_form.save()
            user_add_creation_form.save()

            # username = user_creation_form.cleaned_data.GET('username')
            # password = user_creation_form.cleaned_data.GET('password1')

            # user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("/home")
        else:
            page_contents = dict()
            page_contents['user_forms'] = user_creation_form
            page_contents['user_add_form'] = user_add_creation_form

            return render(request, 'signup.html', page_contents)


class SquadLinkUserLogInView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/home')

        page_contents = dict()
        page_contents['form'] = SquadLinkUserLogInForm(request=request)

        return render(request, 'login.html', page_contents)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/home')

        login_form = SquadLinkUserLogInForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("/home")
            else:
                # user does not exist, redirect to sign up page
                return redirect(SquadLinkUserCreationView.as_view())

        else:
            page_contents = dict()
            page_contents['form'] = login_form

            return render(request, 'login.html', page_contents)


class SquadLinkUserView(View):
    @ login_required
    def get(self, request):
        page_content = dict()
        page_content['user'] = request.user

        return render(request, 'view_profile.html', page_content)
