from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser , ChatRoom
from .models import ChatRoom, ChatMessage

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('student_id', 'name', 'phone_number', 'gender', 'is_verified', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_verified')
    fieldsets = (
        (None, {'fields': ('student_id', 'password')}),
        ('Personal info', {'fields': ('name', 'phone_number', 'gender')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('student_id', 'name', 'phone_number', 'gender', 'password1', 'password2', 'is_active', 'is_staff', 'is_verified')}
        ),
    )
    search_fields = ('student_id', 'name')
    ordering = ('student_id',)

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'departure_time', 'owner', 'created_at')
    search_fields = ('origin', 'destination', 'owner__username')
    list_filter = ('origin', 'destination', 'departure_time', 'created_at')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'message', 'timestamp')
    search_fields = ('user__name', 'message', 'room__origin', 'room__destination')

    def user_name(self, obj):
        return obj.user.name

    def room_info(self, obj):
        return f'{obj.room.origin} to {obj.room.destination}'

    user_name.short_description = 'User Name'
    room_info.short_description = 'Room Info'

admin.site.register(CustomUser, CustomUserAdmin)