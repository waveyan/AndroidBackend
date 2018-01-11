from django.contrib import admin
# from django.contrib.admin.templates.admin import base_
from userapp.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'telephone']
    # list_filter=['created_time']


admin.site.register(User, UserAdmin)
