from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Chat_room

# main view
def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'chat/index.html',{'username': request.user.username, 'id': request.user.id, 'chat_rooms': Chat_room.objects.all()})

# login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')

        else:
            return render(request, 'chat/login.html', {'error': 'Invalid username and password'})
            

    return render(request, 'chat/login.html')

# chat view
def chat_view(request, chat_id):
    # check login
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'chat/chat.html', {'chat_id': chat_id})

def chat_create_form(request):
    # check login
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'chat/chat_create_form.html')

def chat_create(request):
    # check login
    if not request.user.is_authenticated:
        return redirect('login')
    
    name = request.POST['name']
    manager = request.user
    Chat_room.objects.create(name=name, manager=manager)

    id = Chat_room.objects.get(name=name).id

    # redirect to chat/id
    return HttpResponseRedirect('/chat/' + str(id) + '/')