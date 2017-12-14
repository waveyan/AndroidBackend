from django.contrib import admin

from hotspotapp.models import HotSpot


class HotspotAdmin(admin.ModelAdmin):
    list_display = ['name', 'city']
    # list_filter=['created_time']


admin.site.register(HotSpot, HotspotAdmin)
