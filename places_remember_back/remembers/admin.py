from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from remembers.models import RemembersModel


@admin.register(RemembersModel)
class ShopAdmin(OSMGeoAdmin):
    pass
