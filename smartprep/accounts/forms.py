from django import forms
from  django.contrib.auth.forms import  UserCreationForm
from  django.contrib.auth.models import User

# model for defining login form in database
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profiles

class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)


# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model= User
#         fields = ['username', 'email', 'password1', 'password2']

class CreateUserForm(UserCreationForm):
	name = forms.CharField(label = ("Full Name"))
	username = forms.EmailField(label = ("Email"))

	class Meta:
		model = User
		fields = ('name', 'username', 'password1', 'password2')

class ProfileForm(ModelForm):
    class Meta:
        model=Profiles
        fields="__all__"
        exclude=['username','email']

