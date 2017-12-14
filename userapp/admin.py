from django.contrib import admin


from userapp.models import User
class UserAdmin(admin.ModelAdmin):
    list_display=['name','telephone']
    #list_filter=['created_time']

admin.site.register(User, UserAdmin)
