from django.contrib import admin
from models import *

admin.site.register(Region)

class StatisticalDataAdmin(admin.ModelAdmin):
    list_display = ('year', 'component', 'region_area', 'blob')
    search_fields = ['year','component','region__name']
    ordering = ['year','component','region__name']

    def region_area(self, obj):
        return obj.region.name

admin.site.register(StatisticalData, StatisticalDataAdmin)
