from django.contrib import admin

from hotspotapp.models import HotSpot, District, Route


class HotspotAdmin(admin.ModelAdmin):
    list_display = ['name', 'englishname','district','type']
    # list_filter=['created_time']


class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'city']
    # list_filter=['created_time']


class RouteAdmin(admin.ModelAdmin):
    list_display = ['title', 'id']


admin.site.register(HotSpot, HotspotAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Route, RouteAdmin)
