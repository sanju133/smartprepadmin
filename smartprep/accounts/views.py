from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import random
from django.contrib import messages
from .models import UserOTP
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from .models import Profiles
from materials.models import Order
from .forms import ProfileForm


from .forms import CreateUserForm, LoginForm
from accounts.auth import unauthenticated_user

def prac(request):
    return render(request, 'accounts/pracc.html')
def card(request):
    return render(request, 'accounts/card.html')



def homepage(request):
    return render(request, 'accounts/homepage.html')

def contact(request):
    context = {
        'activate_contact': 'active',

    }
    return render(request, 'accounts/contact.html',context)

def about(request):
    context = {
        'activate_about': 'active',

    }
    return render(request, 'accounts/aboutus.html',context)

# def loginpage(request):
#     return render(request,'accounts/login.html')

#
# def Registerpage(request):
#     return render(request,'accounts/register.html')

# function for logout
@login_required
def logout_user(request):
    logout(request)
    return redirect('/login_page')




def register_user(request):
    if request.method == 'POST':
        get_otp = request.POST.get('otp')  # 213243 #None

        if get_otp:
            get_usr = request.POST.get('usr')
            usr = User.objects.get(username=get_usr)
            if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active = True
                usr.save()
                messages.add_message(request, messages.SUCCESS,'Congratulation!Account is created')
                return redirect('/login')
            else:
                messages.add_message(request, messages.ERROR, 'Sorry! You entered wrong OTP')
                return render(request, 'accounts/register.html', {'otp': True, 'usr': usr})

        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            name = form.cleaned_data.get('name').split(' ')

            usr = User.objects.get(username=username)
            usr.email = username
            usr.first_name = name[0]
            if len(name) > 1:
                usr.last_name = name[1]
            usr.is_active = False
            usr.save()
            usr_otp = random.randint(1000, 9999)
            UserOTP.objects.create(user=usr, otp=usr_otp)
            Profiles.objects.create(user=usr , username=usr.username)



            mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

            send_mail(
                "Welcome to Smartprep - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently=False
            )

            return render(request, 'accounts/register.html', {'otp': True, 'usr': usr})


    else:
        form = CreateUserForm()

    return render(request, 'accounts/register.html', {'form': form})

def resend_otp(request):
    if request.method == "GET":
        get_usr = request.GET['usr']
        if User.objects.filter(username = get_usr).exists() and not User.objects.get(username = get_usr).is_active:
            usr = User.objects.get(username=get_usr)
            usr_otp = random.randint(1000, 9999)
            UserOTP.objects.create(user = usr, otp = usr_otp)
            mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

            send_mail(
                "Welcome to Smartprep - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently = False
                )
            return HttpResponse("Resend")

    return HttpResponse("Can't Send ")


@login_required
def logout_user(request):
    logout(request)
    return redirect('/login')



def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        get_otp = request.POST.get('otp') #213243 #None

        if get_otp:
            get_usr = request.POST.get('usr')
            usr = User.objects.get(username=get_usr)
            if int(get_otp) == UserOTP.objects.filter(user = usr).last().otp:
                usr.is_active = True
                usr.save()
                login(request, usr)
                return redirect('/materials/courses/')
            else:
                messages.add_message(request, messages.ERROR, 'Sorry! You entered wrong OTP')
                return render(request, 'accounts/login.html', {'otp': True, 'usr': usr})


        usrname = request.POST['username']
        passwd = request.POST['password']

        user = authenticate(request, username = usrname, password = passwd) #None
        if user is not None:
            login(request, user)
            return redirect('/materials/courses/')
        elif not User.objects.filter(username = usrname).exists():
            messages.add_message(request, messages.ERROR, 'Sorry! Invalid fields')
            return redirect('/login')
        elif not User.objects.get(username=usrname).is_active:
            usr = User.objects.get(username=usrname)
            usr_otp = random.randint(1000, 9999)
            UserOTP.objects.create(user = usr, otp = usr_otp)
            mess = f"Hello {usr.first_name},\nYour OTP is {usr_otp}\nThanks!"

            send_mail(
                "Welcome to ITScorer - Verify Your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [usr.email],
                fail_silently = False
                )
            return render(request, 'accounts/login.html', {'otp': True, 'usr': usr})
        else:
            messages.add_message(request, messages.ERROR, 'Sorry! Invalid fields')
            return redirect('/login')

    form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def profile(request):
    profiles = request.user.profiles
    if request.method== 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profiles)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Profile Updated Successfully')
            return redirect('/profile')
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartItems = order['get_cart_items']
    context = {

        'form': ProfileForm(instance=profiles),
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'accounts/profile.html', context)