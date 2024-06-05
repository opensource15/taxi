from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    gender_choices = [
        ('여성', '여성'),
        ('남성', '남성')
    ]
    gender = forms.ChoiceField(choices=gender_choices, required=True)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('student_id', 'name', 'nickname', 'phone_number', 'gender', 'password1', 'password2')
