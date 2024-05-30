# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    gender_choices = [
        ('여성', '여성'),
        ('남성', '남성')
    ]
    gender = forms.ChoiceField(choices=gender_choices, required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('student_id', 'name', 'phone_number', 'gender', 'password1', 'password2')