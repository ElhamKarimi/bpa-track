from dateutil.parser import parse as date_parser
from django.contrib import admin
from import_export import resources, fields, widgets
from import_export.admin import ImportExportModelAdmin

from bpa_track.users.models import User
from bpa_track.users.admin import UserWidget

from bpa_track.common.models import Facility
from bpa_track.common.admin import (
        FacilityWidget,
        DateField,
        AmpliconAdmin,
        MetagenomicAdmin,
        TransferLogAdmin,
        )

from .models import (
        Amplicon,
        Metagenomic,
        TransferLog
        )

admin.site.register(Amplicon, AmpliconAdmin)
admin.site.register(Metagenomic, MetagenomicAdmin)
admin.site.register(TransferLog, TransferLogAdmin)
