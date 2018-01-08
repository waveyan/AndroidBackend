from django.contrib import admin

from activityapp.models import Activity


class ActivityAdmin(admin.ModelAdmin):
    list_display = ['title','id', 'subject','hotspot','telephone']
    # list_filter=['created_time']


admin.site.register(Activity, ActivityAdmin)
