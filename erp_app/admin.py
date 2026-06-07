from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Group, Payment, SupportTicket, ChatMessage

class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'middle_name', 'role', 'is_active', 'date_joined')
    list_filter = ('is_active', 'role', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'middle_name')
    ordering = ('-date_joined',)
    actions = ['approve_users']

    def approve_users(self, request, queryset):
        queryset.update(is_active=True)
    approve_users.short_description = "Tanlangan foydalanuvchilarni tasdiqlash (is_active=True)"

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Qo\'shimcha ma\'lumotlar', {'fields': ('role', 'middle_name', 'phone_number')}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(Group)
admin.site.register(Payment)
admin.site.register(SupportTicket)
admin.site.register(ChatMessage)