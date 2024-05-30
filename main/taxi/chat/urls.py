from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),  # 홈 페이지 또는 기본 경로 추가
]