from django.contrib import admin
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from .models import (
        Facility,
        Amplicon,
        Metagenomic,
        TransferLog
        )

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


class DateField(fields.Field):
    """
    This field automatically parses a number of known date formats and returns
    the standard python date
    """

    def __init__(self, *args, **kwargs):
        super(DateField, self).__init__(*args, **kwargs)

    def clean(self, data):
        return date_parser(data[self.column_name])



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

class AmpliconAdmin(ImportExportModelAdmin):
    resource_class = AmpliconResource
    list_display = ('extraction_id', 'facility', 'target', 'metadata_filename', 'comments')
    list_filter = ('facility', 'target', )
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

class MetagenomicAdmin(ImportExportModelAdmin):
    resource_class = MetagenomicResource
    list_display = ('extraction_id', 'facility', 'metadata_filename', 'comments')
    list_filter = ('facility',)
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

class TransferLogAdmin(ImportExportModelAdmin):
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

    list_filter = (
            'facility',
            'transfer_to_facility_date',
            'transfer_to_archive_date',
            'data_type',
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
