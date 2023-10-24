from django.contrib import admin
from accounts.models import Organizer, Attendee , User
from django.contrib.auth.admin import UserAdmin
# Register your models here.


@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    pass

@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    pass

class CustomUserAdmin(UserAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
# admin.site.register(User, CustomUserAdmin)