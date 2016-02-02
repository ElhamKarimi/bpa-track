from dateutil.parser import parse as date_parser
from django.contrib import admin
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from bpa_track.users.models import User
from bpa_track.users.admin import UserWidget

from bpa_track.common.models import Facility
from bpa_track.common.admin import FacilityWidget

from .models import SampleReceived, Amplicon, Metagenomic

class DateField(fields.Field):
    """
    This field automatically parses a number of known date formats and returns
    the standard python date
    """

    def __init__(self, *args, **kwargs):
        super(DateField, self).__init__(*args, **kwargs)

    def clean(self, data):
        return date_parser(data[self.column_name])



class SampleReceivedResource(resources.ModelResource):
    extraction_id = fields.Field(attribute='extraction_id', column_name='Sample extraction ID')
    batch_number = fields.Field(attribute='batch_number', column_name='Batch number')
    date_received = DateField(attribute='date_received', column_name='Date received')

    submitter = fields.Field(
            attribute='submitter',
            column_name='Submitter Name',
            widget=UserWidget()
            )

    facility= fields.Field(
            attribute='facility',
            column_name='Facility',
            widget=FacilityWidget()
            )

    class Meta:
        model = SampleReceived
        import_id_fields = ('extraction_id', )
        export_order = (
                'extraction_id',
                'facility',
                'batch_number',
                'date_received',
                'submitter')

@admin.register(SampleReceived)
class SampleReceivedAdmin(ImportExportModelAdmin):
    resource_class = SampleReceivedResource
    list_display = (
            'extraction_id',
            'facility',
            'batch_number',
            'date_received',
            'submitter')

    date_hierarchy = 'date_received'
    search_fields = ('extraction_id', 'facility__name', 'submitter__name', 'date_received', 'batch_number')



class AmpliconResource(resources.ModelResource):
    extraction_id = fields.Field(attribute='extraction_id', column_name='Sample extraction ID')
    target = fields.Field(attribute='target', column_name='Target')
    comments = fields.Field(attribute='comments', column_name='Comments')
    facility = fields.Field(
            attribute='facility',
            column_name='Facility',
            widget=FacilityWidget()
            )

    class Meta:
        model = Amplicon
        import_id_fields = ('extraction_id', )
        export_order = (
                'extraction_id',
                'target',
                'facility',
                'comments')

@admin.register(Amplicon)
class AmpliconAdmin(ImportExportModelAdmin):
    resource_class = AmpliconResource
    list_display = ('extraction_id', 'facility', 'target', 'comments')
    search_fields = ('extraction_id', 'facility__name', 'target', 'comments')


class MetagenomicResource(resources.ModelResource):
    extraction_id = fields.Field(attribute='extraction_id', column_name='Sample extraction ID')
    facility = fields.Field(
            attribute='facility',
            column_name='Facility',
            widget=FacilityWidget()
            )
    comments = fields.Field(attribute='comments', column_name='Comments')

    class Meta:
        model = Amplicon
        import_id_fields = ('extraction_id', )
        export_order = (
                'extraction_id',
                'facility',
                'comments')

@admin.register(Metagenomic)
class AmpliconAdmin(ImportExportModelAdmin):
    resource_class = MetagenomicResource
    list_display = ('extraction_id', 'facility', 'comments')
    search_fields = ('extraction_id', 'facility__name', 'comments')

