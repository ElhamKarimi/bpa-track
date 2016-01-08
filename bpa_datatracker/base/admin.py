from dateutil.parser import parse as date_parser
from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin

from .models import SampleReception

class DateField(fields.Field):
    def __init__(self, *args, **kwargs):
        super(DateField, self).__init__(*args, **kwargs)

    def clean(self, data):
        return date_parser(data[self.column_name])

class SampleReceptionResource(resources.ModelResource):

    vendor = fields.Field(attribute='vendor', column_name='Vendor')
    extraction_id = fields.Field(attribute='extraction_id', column_name='Sample extraction ID')
    batch_number = fields.Field(attribute='batch_number', column_name='Batch number')
    submitter = fields.Field(attribute='submitter__name', column_name='Submitter Name')
    # date_received = fields.Field(attribute='date_received', column_name='Date received')
    date_received = DateField(attribute='date_received', column_name='Date received')

    class Meta:
        model = SampleReception
        import_id_fields = ('extraction_id',)


class SampleReceptionAdmin(ImportExportModelAdmin):
    resource_class = SampleReceptionResource

admin.site.register(SampleReception, SampleReceptionAdmin)
