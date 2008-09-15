from django.contrib import admin
from django.contrib.gis.admin import GeoModelAdmin
from world_locations.models import Country, SubdivisionType, Subdivision, Location


admin.site.register(Country)
admin.site.register(SubdivisionType)
admin.site.register(Subdivision)
admin.site.register(Location)
