from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group, auth
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import PropertyForm
from .models import Property


def home(request):

    if request.user.is_authenticated:
        return redirect(property_listing)
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

                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email
                )
                user.save()

                lurker_group = Group.objects.get(name='lurker') 
                lurker_group.user_set.add(user)

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
def upload_property(request):
    if request.method == 'POST':

        name = request.POST['name']
        area = request.POST['area']
        city = request.POST['city']
        property_type = request.POST['property_type']
        bhk_type = request.POST['bhk_type']
        list_type = request.POST['list_type']
        description = request.POST['description']
        rent = request.POST['rent']
        deposit = request.POST['deposit']
        available_from = request.POST['available_from']
        owner_name = request.POST['owner_name']
        ph_contact = request.POST['ph_contact']
        publisher = request.user

        property = Property.objects.create(
            name=name,
            area=area,
            city=city,
            property_type=property_type,
            bhk_type=bhk_type,
            list_type=list_type,
            description=description,
            rent=rent,
            deposit=deposit,
            available_from=available_from,
            owner_name=owner_name,
            ph_contact=ph_contact,
            publisher=publisher
        )

        property.save()
        msg = ('Your property listing submitted. '
            'Once the moderator approves your listing, '
            'it will be visible to all users')
        messages.info(request, msg)
        return redirect(my_listing)
    else:

        form = PropertyForm()
        context = {
            'title': 'List Property',
            'form':form
        }
        return render(request, 'app/upload_property.html', context)


@login_required(login_url='login')
def property_listing(request):

    properties = Property.objects.filter(is_active=True, is_approved=True).order_by("-publish_date")

    context = {
        'title': 'Available Properties',
        'properties': properties
    }

    return render(request, 'app/property_listing.html', context)


@login_required(login_url='login')
def property_approvals(request, property_id=None):

    user_groups = list(request.user.groups.values_list('name', flat = True))

    if "moderator" not in user_groups:
        return redirect(property_listing)

    if property_id != None:
        property = Property.objects.get(id=property_id, is_active=True)

        if not property:
            return HttpResponse('Property you were trying to approve was removed by the publisher!')

        property.is_approved = True
        property.approver = request.user
        property.approved_date = timezone.now()
        property.save()

        return HttpResponse('Property Successfully Approved')

    else:
        properties = Property.objects.filter(is_active=True, is_approved=False).order_by("-publish_date")

        context = {
            'title': 'Approve Properties',
            'properties': properties
        }
        
        return render(request, 'app/property_requests.html', context)


@login_required(login_url='login')
def my_listing(request):

    properties = Property.objects.filter(publisher=request.user, is_active=True).order_by("-publish_date")

    user_groups = list(request.user.groups.values_list('name', flat = True))
    is_moderator = False
    if "moderator" in user_groups:
        is_moderator = True
        
    context = {
        'title': 'My Listings',
        'properties': properties,
        'is_moderator': is_moderator
    }

    return render(request, 'app/my_listing.html', context)


@login_required(login_url='login')
def delete_my_listing(request, property_id):

    property = Property.objects.get(id=property_id, is_active=True, publisher=request.user)

    if not property:
        return HttpResponse('Property you were trying to delete, does not exists!')

    property.is_active = False
    property.save()

    msg = ('Your property listing deleted. '
            'Contact admin, if this was a mistake.')
    messages.info(request, msg)
    return redirect(my_listing)


