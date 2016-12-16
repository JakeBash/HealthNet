# File: admin.py
# Description: This file contains the Django model imports for the admin console
# Author(s): Team Suites (1)

# imports
from django.contrib import admin
from .models import Patient
from .models import Doctor
from .models import Nurse
from .models import Administrator
from .models import Hospital
from .models import LogInInfo
from .models import Prescription
from .models import Appointment
from .models import Test
from .models import EmergencyContact
from .models import Message

# model registers
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Nurse)
admin.site.register(Administrator)
admin.site.register(Hospital)
admin.site.register(LogInInfo)
admin.site.register(Prescription)
admin.site.register(Appointment)
admin.site.register(Test)
admin.site.register(EmergencyContact)
admin.site.register(Message)
