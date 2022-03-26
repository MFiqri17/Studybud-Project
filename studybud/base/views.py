import imp
from urllib.request import Request
from django.shortcuts import render, redirect
from django.template import context
from .models import *
from .forms import RoomForm, MyUserCreationForm, UserForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    room_total = Room.objects.all().count()
    
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    
    room_messages = Message.objects.all()
    
    topics = Topic.objects.all()
    
    context = {'rooms':rooms, 'topics':topics, 'room_total':room_total, 'messages':room_messages}
    
    return render(request, 'base/home.html', context)



def room(request, pk):
    rooms = Room.objects.get(id = pk)
    room_messages = rooms.message_set.all()
    participants_total = rooms.participants.all().count()
    participant = rooms.participants.all()
    if request.method == 'POST':
        body_message = request.POST.get('body_message')
        Message.objects.create(
            user = request.user,
            room = rooms,
            body = body_message
        )
        rooms.participants.add(request.user)
        return redirect('room', pk=rooms.id)
    context = {'rooms':rooms, 'room_messages':room_messages, 'participants_total':participants_total, 'participant':participant}
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
            
        return redirect('home')
            
    context = {'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context)         



def updateRoom(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request, 'base/room_form.html', context)   


def deleteRoom(request, pk):
    room = Room.objects.get(id = pk)
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    
    return render(request, 'base/delete.html', {'obj':room})    


def registerPage(request):
    form = MyUserCreationForm()
    
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        

    
    return render(request, 'base/login_register.html', {'form': form}) 

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')   
            
        user = authenticate(request, email=email, password=password)     
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password does not exist')
            
    context = {'page': page}
    return render(request, 'base/login_register.html', context)   

def logoutUser(request):
    logout(request)
    return redirect('home')     


def profilePage(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()  
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)  


def editProfile(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=user.id)    
        
        
    
    return render(request, 'base/update_user.html', {'form':form})
    
    
    