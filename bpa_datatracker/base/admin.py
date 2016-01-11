from dateutil.parser import parse as date_parser
from django.contrib import admin
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from bpa_datatracker.users.models import User
from .models import SampleReceived

class DateField(fields.Field):
    """
    This field automatically parses a number of known date formats and returns
    the standard python date
    """

    def __init__(self, *args, **kwargs):
        super(DateField, self).__init__(*args, **kwargs)

    def clean(self, data):
        return date_parser(data[self.column_name])

class UserWidget(widgets.ForeignKeyWidget):
    def __init__(self):
        self.model = User
        self.username = ""
        self.firstname = ""
        self.lastname = ""

    def _set_name(self, name_from_source):
        "use first letter from first name and whole of last name, eurocentric"

        parts = name_from_source.lower().split()
        if len(parts) >= 2:
            self.firstname = parts[0]
            self.lastname = parts[-1]
            self.username = self.firstname[0] + self.lastname
        else:
            self.firstname = parts[0]
            self.lastname = parts[0]
            self.username = self.lastname


    def clean(self, value):
        self._set_name(value)

        user, _ = self.model.objects.get_or_create(
                first_name=self.firstname,
                last_name=self.lastname,
                username=self.username)

        return user

    def render(self, value):
        return value


class SampleReceivedResource(resources.ModelResource):

    vendor = fields.Field(attribute='vendor', column_name='Vendor')
    extraction_id = fields.Field(attribute='extraction_id', column_name='Sample extraction ID')
    batch_number = fields.Field(attribute='batch_number', column_name='Batch number')
    date_received = DateField(attribute='date_received', column_name='Date received')

    submitter = fields.Field(
            attribute='submitter',
            column_name='Submitter Name',
            # widget=widgets.ForeignKeyWidget(User, field="username"))
            widget=UserWidget()
            )

    class Meta:
        model = SampleReceived
        import_id_fields = ('extraction_id', )
        export_order = (
                'extraction_id',
                'vendor',
                'batch_number',
                'date_received',
                'submitter')

@admin.register(SampleReceived)
class SampleReceivedAdmin(ImportExportModelAdmin):
    resource_class = SampleReceivedResource
    list_display = (
            'vendor',
            'extraction_id',
            'batch_number',
            'date_received',
            'submitter')
    date_hierarchy = 'date_received'
    empty_value_display = '-empty-'

