# -*- coding: utf-8 -*-
from django.db import models
from bpa_track.users.models import User
from bpa_track.common.models import (
        Facility,
        TransferLog,
        Amplicon,
        Metagenomic,
        )

class TransferLog(TransferLog):
    pass

class Metagenomic(Metagenomic):
    pass

class Amplicon(Amplicon):
    pass
