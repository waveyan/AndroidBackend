from django.contrib import admin

from hotspotapp.models import HotSpot, District, Route,City


class HotspotAdmin(admin.ModelAdmin):
    list_display = ['name', 'englishname','district','type']
    # list_filter=['created_time']


class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'city','city_obj']
    # list_filter=['created_time']


class RouteAdmin(admin.ModelAdmin):
    list_display = ['title', 'id']

class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


admin.site.register(HotSpot, HotspotAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(City,CityAdmin);
