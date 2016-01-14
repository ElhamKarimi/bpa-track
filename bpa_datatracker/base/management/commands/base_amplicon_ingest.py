# -*- coding: utf-8 -*-

"""
Ingests BASE Amplicon metadata from server into database.
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from ...models import Amplicon

from django.db.utils import DataError
from unipath import Path
import logging
import os

from libs.excel_wrapper import ExcelWrapper
from libs.fetch_data import Fetcher

from bpa_datatracker.common.models import Facility
from bpa_datatracker.base.models import Amplicon

METADATA_ROOT = os.path.join(os.path.expanduser('~'), 'bpametadata')

METADATA_URL = "https://downloads.bioplatforms.com/base/tracking/amplicons/"
DATA_DIR = Path(METADATA_ROOT, "base/amplicon_metadata/")


class Command(BaseCommand):
    help = 'Ingest BASE Amplicons'

    def _get_data(self, file_name):
        """ The data sets is relatively small, so make a in-memory copy to simplify some operations. """

        field_spec = [
                ("sample_extraction_id", "Sample extraction ID", None),
                ("sequencing_facility", "Sequencing facility", None),
                ("target", "Target", lambda s: s.upper().strip()),
                ]

        wrapper = ExcelWrapper(field_spec,
                file_name,
                sheet_name="Sheet1",
                header_length=4,
                column_name_row_index=1,
                formatting_info=True,
                pick_first_sheet=True)

        return wrapper.get_all()


    def _get_facility(self, entry):
        name = entry.sequencing_facility
        if name is None:
            name = "UNKNOWN"

        name = name.strip()
        if name == "":
            name = "UNKNOWN"
        facility, _ = Facility.objects.get_or_create(name=name)
        return facility


    def _add_samples(self, data):
        """ Add sequence files """

        for entry in data:
            comment = "Amplicon sequence noted in {}".format(entry.file_name)
            amplicon, _ = Amplicon.objects.get_or_create(
                    sample_extraction_id=entry.sample_extraction_id,
                    sequencing_facility=self._get_facility(entry),
                    target=entry.target,
                    comments=comment
                    )

    def _do_metadata(self):
        def is_metadata(path):
            if path.isfile() and path.ext == ".xlsx":
                return True

        self.stdout.write(self.style.SUCCESS("Ingesting BASE Amplicon metadata from {0}".format(DATA_DIR)))
        for metadata_file in DATA_DIR.walk(filter=is_metadata):
            self.stdout.write(self.style.SUCCESS("Processing BASE Amplicon Metadata file {0}".format(metadata_file)))
            samples = list(self._get_data(metadata_file))
            self._add_samples(samples)


    def handle(self, *args, **options):
        fetcher = Fetcher(DATA_DIR, METADATA_URL, auth=("base", "b4s3"))
        fetcher.clean()
        fetcher.fetch_metadata_from_folder()

        # find all the spreadsheets in the data directory and ingest them
        self._do_metadata()
