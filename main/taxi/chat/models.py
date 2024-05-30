from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, student_id, password=None, **extra_fields):
        if not student_id:
            raise ValueError('The Student ID field must be set')
        user = self.model(student_id=student_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, student_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(student_id, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)  # 새 필드 추가

    objects = CustomUserManager()

    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS = ['name', 'phone_number', 'gender']

    def __str__(self):
        return self.student_id

class ChatRoom(models.Model):
    origin = models.CharField(max_length=255)  # 출발지
    destination = models.CharField(max_length=255)  # 도착지
    departure_time = models.DateTimeField()  # 출발시간
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='owned_rooms', on_delete=models.CASCADE)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='ChatRoomMembership', related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.origin} to {self.destination} at {self.departure_time}'

class ChatRoomMembership(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.name} in {self.room.origin} to {self.room.destination}'

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message[:20]}'