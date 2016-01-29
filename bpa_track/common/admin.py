from django.contrib import admin
from import_export import resources, fields, widgets

from .models import Facility

class FacilityWidget(widgets.ForeignKeyWidget):
    def __init__(self):
        self.model = Facility
        self.field = "name"

    def clean(self, value):
        facility, _ = self.model.objects.get_or_create(name=value)
        return facility

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = (
            'name',
            'note'
            )
