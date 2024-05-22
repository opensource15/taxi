from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login_view/', views.login_view, name='login_view'),
    path('chat_create_form/', views.chat_create_form, name='chat_create_form'),
    path('chat_create/', views.chat_create, name='chat_create'),
    path('<str:chat_id>/', views.chat_view, name='chat_view'),
]