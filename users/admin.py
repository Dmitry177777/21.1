from django.contrib import admin
from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'avatar','phone', 'country',)
    search_fields = ('email', 'phone','country',)
    list_filter = ('avatar', )



