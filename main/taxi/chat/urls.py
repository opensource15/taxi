from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('not_verified/', views.not_verified, name='not_verified'),
    path('newroom/', views.newroom, name='newroom'),
    path('', views.home, name='home'),  # 홈 페이지 또는 기본 경로 추가
    path('chatrooms/<int:room_id>/', views.chatroom_detail, name='chatroom_detail'),
    path('logout', views.logout_view, name='logout'),
    path('api/messages/<int:room_id>/', views.chat_messages, name='chat_messages'),  # API 엔드포인트 추가
    path('update_charge/<int:room_id>/', views.update_charge, name='update_charge'),
]