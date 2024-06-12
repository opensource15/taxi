from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django import forms
from django.utils import timezone
from .models import CustomUser, ChatRoom, ChatRoomMembership, ChatMessage
from django.http import JsonResponse
from django.contrib.auth.views import LoginView 
from django.views.decorators.http import require_http_methods
import json
from django.views.decorators.csrf import csrf_exempt

class CustomLoginView(LoginView):
    template_name = 'chat/login.html'



@login_required
def home(request):
    if not request.user.is_verified:
        return redirect('not_verified')
    
    now = timezone.now()
    chatrooms = ChatRoom.objects.all()

    search_query = request.GET.get('destination', '')
    if search_query:
        chatrooms = chatrooms.filter(destination__icontains=search_query)
        search_result = f"\"{search_query}\"로 가는 채팅방입니다."
    else:
        search_result = "지금 모집 중인 채팅방"

    chatrooms = [room for room in chatrooms if room.departure_time > now]

    context = {
        'chatrooms': chatrooms,
        'search_result': search_result,
    }
    return render(request, 'chat/home.html', context)


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            
            user = form.save()
            user.is_verified = False  # 새 사용자에 대한 기본 설정
            user.save()
            login(request, user)
            return redirect('home')  # 성공 페이지 또는 로그인 페이지로 리디렉션
        
        if not form.is_valid():
            print("에러출력")
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    return render(request, 'chat/signup.html', {'form': form})

@login_required
def not_verified(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    if request.user.is_verified:
        return redirect('home')
    return render(request, 'chat/not_verified.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import ChatRoom
from datetime import datetime

@login_required
def newroom(request):
    if not request.user.is_verified:
        return redirect('not_verified')
    
    if request.method == 'POST':
        origin = request.POST.get('origin')
        destination = request.POST.get('destination')
        date = request.POST.get('date')
        time = request.POST.get('time')

        # Combine date and time into a single datetime object
        departure_time = datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M')

        chatroom = ChatRoom.objects.create(
            origin=origin,
            destination=destination,
            departure_time=departure_time,
            owner=request.user
        )
        chatroom.members.add(request.user)
        chatroom.save()
        
        return redirect('chat:chatroom_detail', room_id=chatroom.id)  # URL 이름 수정
    
    context = {
        'today': timezone.now()
    }
    return render(request, 'chat/newroom.html', context)


@login_required
def chatroom_detail(request, room_id):
    chatroom = get_object_or_404(ChatRoom, id=room_id)

    # Add user to the chatroom if not already a member
    if not ChatRoomMembership.objects.filter(user=request.user, room=chatroom).exists():
        ChatRoomMembership.objects.create(user=request.user, room=chatroom)

    context = {
        'chatroom': chatroom,
    }
    return render(request, 'chat/chatroom_detail.html', context)

@login_required
@csrf_exempt
@require_http_methods(["GET", "POST"])
def chat_messages(request, room_id):
    chatroom = get_object_or_404(ChatRoom, id=room_id)

    if request.method == 'GET':
        messages = chatroom.messages.all().order_by('timestamp')
        message_list = [{
            'nickname': message.user.nickname,
            'student_id' : message.user.student_id,
            'message': message.message,
            'timestamp': message.timestamp.isoformat()  # ISO 포맷으로 전송
        } for message in messages]
        return JsonResponse({'messages': message_list})

    elif request.method == 'POST':
        print(request.body)
        data = json.loads(request.body.decode('utf-8'))
        message_text = data.get('message')
        user = request.user

        if not message_text:
            return JsonResponse({'error': 'Invalid data'}, status=400)

        message = ChatMessage.objects.create(
            room=chatroom,
            user=user,
            message=message_text
        )
        return JsonResponse({
            'nickname': message.user.nickname,
            'student_id' : message.user.student_id,
            'message': message.message,
            'timestamp': message.timestamp.isoformat()  # ISO 포맷으로 전송
        })
    
def logout_view(request):
    logout(request)
    return redirect('home')

@csrf_exempt
def update_charge(request, room_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        charge = data.get('charge')
        chatroom = get_object_or_404(ChatRoom, id=room_id)
        chatroom.charge = charge
        chatroom.save()
        return JsonResponse({'status': 'success'})
