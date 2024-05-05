from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Record, Profile

class UserProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'
    
class AccountsUserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
        
admin.site.unregister(User)
admin.site.register(User, AccountsUserAdmin)
admin.site.register(Profile)

admin.site.register(Record)
