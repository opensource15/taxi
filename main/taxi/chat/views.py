from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django import forms
from .models import CustomUser
from django.contrib.auth.views import LoginView  # 여기에 추가

class CustomLoginView(LoginView):
    template_name = 'chat/login.html'

def home(request):
    return render(request, 'chat/home.html')


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