from ast import Mod
from dataclasses import field
from pyexpat import model
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host' , 'participants']

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password1', 'password2']    
        
        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'bio', 'avatar']         