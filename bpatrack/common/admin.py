
from dateutil.parser import parse as date_parser
from django.contrib import admin
from django.utils.html import format_html
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

JIRA_URL = "https://ccgmurdoch.atlassian.net/projects/BRLOPS/issues/"

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


# Amplicon
class CommonAmpliconResource(resources.ModelResource):
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
        abstract = True
        import_id_fields = ('extraction_id', )
        export_order = (
                'extraction_id',
                'target',
                'facility',
                'metadata_filename',
                'comments')

class CommonAmpliconAdmin(ImportExportModelAdmin):
    list_display = ('extraction_id', 'facility', 'target', 'metadata_filename', 'comments')
    list_filter = ('facility', 'target', )
    search_fields = ('extraction_id', 'facility__name', 'target', 'comments')


# Metagenomics
class CommonMetagenomicResource(resources.ModelResource):
    extraction_id = fields.Field(attribute='extraction_id', column_name='Sample extraction ID')
    facility = fields.Field(
            attribute='facility',
            column_name='Facility',
            widget=FacilityWidget()
            )
    comments = fields.Field(attribute='comments', column_name='Comments')

    class Meta:
        abstract = True
        import_id_fields = ('extraction_id', )
        export_order = (
                'extraction_id',
                'facility',
                'metadata_filename',
                'comments')

class CommonMetagenomicAdmin(ImportExportModelAdmin):
    list_display = ('extraction_id', 'facility', 'metadata_filename', 'comments')
    list_filter = ('facility',)
    search_fields = ('extraction_id', 'facility__name', 'comments')


# TransferLog
class CommonTransferLogResource(resources.ModelResource):
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
        abstract = True
        import_id_fields = ('folder_name', )


class CommonTransferLogAdmin(ImportExportModelAdmin):

    def show_downloads_url(self, obj):
        try:
            short = obj.downloads_url.split("/")[-2]
            return format_html("<a href='{url}'>{short}</a>", url=obj.downloads_url, short=short)
        except IndexError:
            return ""

    show_downloads_url.short_description = "Downloads URL"
    show_downloads_url.allow_tags = True

    def show_ticket_url(self, obj):
        jurl = JIRA_URL + obj.ticket_url
        return format_html("<a href='{jurl}'>{url}</a>", url=obj.ticket_url, jurl=jurl)

    show_ticket_url.short_description = "Ticket URL"
    show_ticket_url.allow_tags = True

    date_hierarchy = 'transfer_to_archive_date'

    list_display = (
            'facility',
            'transfer_to_facility_date',
            'description',
            'data_type',
            'folder_name',
            'transfer_to_archive_date',
            'notes',
            'show_ticket_url',
            'show_downloads_url'
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


class CommonDataSetAdmin(ImportExportModelAdmin):
    date_hierarchy = 'transfer_to_archive_date'

    list_display = (
            'name',
            'facility',
            'transfer_to_archive_date',
            'ticket_url',
            'downloads_url',
            'note')

    list_filter = ('facility',)
    search_fields = ('facility__name', 'comments', )
