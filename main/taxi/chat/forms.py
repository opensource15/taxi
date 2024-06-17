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
    student_id_file = forms.ImageField(required=False)  # 여기서 필드를 필수로 설정하지 않음

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def clean(self):
        cleaned_data = super().clean()
        student_id_file = cleaned_data.get("student_id_file") # 
        if not student_id_file:
            raise ValidationError({'student_id_file': "파일이 유효하지 않습니다."}) # 가끔 파일 경로 이상할 때 발생... 해결법은 모르겠습니다.
        return cleaned_data

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('student_id', 'name', 'nickname', 'phone_number', 'gender', 'student_id_file', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['student_id_file'].required = False
