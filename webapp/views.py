from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

def home(request):

    if request.user.is_authenticated:
        return redirect(workspace)
    return render(request, 'user/home.html', {'title': 'home'})


def register(request):
    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:

            if User.objects.filter(username=username).exists():

                messages.info(request, 'Username is already taken')
                return redirect(register)

            elif User.objects.filter(email=email).exists():

                messages.info(request, 'Email is already taken')
                return redirect(register)

            else:

                User.objects.create_user(
                    username=username,
                    password=password,
                    email=email
                ).save()

                return redirect('login')

        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect(register)

    else:
        return render(request, 'user/register.html', {'title': 'Register'})


def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('home')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('login')
    else:
        return render(request, 'user/login.html', {'title': 'Login'})


def logout(request):
    auth.logout(request)
    return redirect('home')


# private views

@login_required(login_url='login')
def workspace(request):

    return render(request, 'app/workspace.html', {'title': 'Workspace'})


@login_required(login_url='login')
def workspace_preference(request):

    return render(request, 'app/workspace_preference.html', {'title': 'Workspace Preferences'})
