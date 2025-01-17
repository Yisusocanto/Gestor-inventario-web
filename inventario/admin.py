from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.
class CustomUserAdmin(UserAdmin):
    # Añade 'rol' a los campos mostrados
    list_display = ('username', 'email', 'first_name', 'last_name', 'rol', 'is_staff')
    # Añade 'rol' a los campos que se pueden editar
    fieldsets = UserAdmin.fieldsets + (
        ('Rol de Usuario', {'fields': ('rol',)}),
    )

admin.site.register(User, CustomUserAdmin)