from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from.models import profile, message, group_message, Group


class SignUP(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']


class UserF(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileF(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['image', 'Searching_Name', "interest"]


class msg(forms.ModelForm):
    class Meta:
        model = message
        fields = "__all__"
        exclude = ('receiver', 'Sender')


class groupform(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name', 'group_image', 'topic']


class Group_msg(forms.ModelForm):
    class Meta:
        model = group_message
        fields = ('message', 'image', 'file')
