from django.contrib.auth.models import User
from django.db import models

# Create your models here
class Chat_room(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Chat_message(models.Model):
    room = models.ForeignKey(Chat_room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.message

