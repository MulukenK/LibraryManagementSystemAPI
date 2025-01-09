from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm 
from .models import CustomUser, Book, Transaction

class CustomUserAdmin(UserAdmin): 
    add_form = CustomUserCreationForm 
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [ 
        "email",
        "date_of_membership",
        "is_active",
        ]
    
fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("email",)}),) 
add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("email",)}),)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book)