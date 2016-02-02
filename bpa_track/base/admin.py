from dateutil.parser import parse as date_parser
from django.contrib import admin
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from bpa_track.users.models import User
from bpa_track.users.admin import UserWidget

from bpa_track.common.models import Facility
from bpa_track.common.admin import FacilityWidget

from .models import SampleReceived, Amplicon, Metagenomic, TransferLog

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
    metadata_filename = fields.Field('metadata_filename', column_name='Metadata Filename')
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
                'submitter',
                'metadata_filename',
                )

@admin.register(SampleReceived)
class SampleReceivedAdmin(ImportExportModelAdmin):
    resource_class = SampleReceivedResource
    list_display = (
            'extraction_id',
            'facility',
            'batch_number',
            'date_received',
            'submitter',
            )

    date_hierarchy = 'date_received'
    search_fields = ('extraction_id', 'facility__name', 'submitter__name', 'date_received', 'batch_number')



class AmpliconResource(resources.ModelResource):
    extraction_id = fields.Field(attribute='extraction_id', column_name='Sample extraction ID')
    target = fields.Field(attribute='target', column_name='Target')
    comments = fields.Field(attribute='comments', column_name='Comments')
    metadata_filename = fields.Field('metadata_filename', column_name='Metadata Filename')
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
                'metadata_filename',
                'comments')

@admin.register(Amplicon)
class AmpliconAdmin(ImportExportModelAdmin):
    resource_class = AmpliconResource
    list_display = ('extraction_id', 'facility', 'target', 'metadata_filename', 'comments')
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
                'metadata_filename',
                'comments')

@admin.register(Metagenomic)
class AmpliconAdmin(ImportExportModelAdmin):
    resource_class = MetagenomicResource
    list_display = ('extraction_id', 'facility', 'metadata_filename', 'comments')
    search_fields = ('extraction_id', 'facility__name', 'comments')


class TransferLogResource(resources.ModelResource):
    facility = fields.Field(
            attribute='facility',
            column_name='Sequencing facility',
            widget=FacilityWidget()
            )
    transfer_to_facility_date = DateField(
            attribute='transfer_to_facility_date',
            column_name='Date of transfer')
    description = fields.Field(attribute='description', column_name='Description')
    data_type = fields.Field(attribute='data_type', column_name='Data type')
    folder_name = fields.Field(attribute='folder_name', column_name='Folder name')
    transfer_to_archive_date = DateField(
            attribute='transfer_to_archive_date',
            column_name='Date of transfer to archive')
    notes = fields.Field(attribute='notes', column_name='Notes')
    ticket_url = fields.Field(attribute='ticket_url', column_name='CCG JIRA Ticket')
    downloads_url = fields.Field(attribute='downloads_url', column_name='Download')

    class Meta:
        model = TransferLog
        import_id_fields = ('folder_name', )

@admin.register(TransferLog)
class AmpliconAdmin(ImportExportModelAdmin):
    resource_class = TransferLogResource
    date_hierarchy = 'transfer_to_archive_date'

    list_display = (
            'facility',
            'transfer_to_facility_date',
            'description',
            'data_type',
            'folder_name',
            'transfer_to_archive_date',
            'notes',
            'ticket_url',
            'downloads_url'
            )

    search_fields = (
            'facility__name',
            'transfer_to_facility_date',
            'description',
            'data_type',
            'folder_name',
            'transfer_to_archive_date',
            'notes',
            'ticket_url',
            'downloads_url'
            )
