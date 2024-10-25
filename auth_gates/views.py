from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import UserLoginForm, RegistrationForm


def authenticate_user(request):

    login_form = UserLoginForm()
    register_form = RegistrationForm()
    next_url = request.GET.get('next', reverse_lazy('invoicer:clients_list'))

    if request.method == 'POST':

        if "login_form_submit" in request.POST:

            login_form = UserLoginForm(data=request.POST)

            if login_form.is_valid():

                user = authenticate(request, username=request.POST['username'],
                                    password=request.POST['password'])

                if user is not None:
                    # If the user is authenticated correctly
                    login(request, user)
                    return redirect(next_url)

        elif "register_form_submit" in request.POST:

            register_form = RegistrationForm(request.POST)

            if register_form.is_valid():

                new_user = register_form.save()

                login(request, new_user)

                return redirect(next_url)

    if not request.user.is_authenticated:
        return render(
            request,
            'auth_gates/authenticate_user.html',
            {
                'login_form': login_form,
                'register_form': register_form,
                'next': next_url
            }
        )
    else:
        return redirect(next_url)


@login_required(login_url='/auth/login/')
def logout_user(request):
    # It is super important to only execute this function if the request is
    # POST request.
    if request.method == 'POST':
        logout(request)
        return redirect('invoicer:home')
