# File: models.py
# Description: This file contains Python and Django code which will form the Model element
#              of the Model-Template-Controller (MTC) design pattern.
# Author(s): Team Suites (1)

# imports
from django.db import models
from datetime import date


# This module contains the Hospital model.
class Hospital(models.Model):
    name = models.CharField(max_length=50, default='')
    address = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name


# This module contains the Emergency Contact model.
class EmergencyContact(models.Model):
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    number = models.CharField(max_length=13, default='')
    address = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.firstName + " " + self.lastName


# This module contains the Patient model.
class Patient(models.Model):
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    number = models.CharField(max_length=13, default='')
    address = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')
    provider = models.CharField(max_length=100, default='')
    insuranceid = models.CharField(max_length=12, default='')
    contact = models.ForeignKey(EmergencyContact, null=True)
    height = models.CharField(max_length=7, default='')
    weight = models.CharField(max_length=6, default='')
    allergies = models.TextField(max_length=500, default='')
    gender = models.CharField(max_length=23, default='')
    username = models.CharField(max_length=30, default='')
    hospital = models.ForeignKey(Hospital, default=None, blank=True, null=True)

    def __str__(self):
        return self.firstName + " " + self.lastName

    def getEmergencyContact(self, patient):
        return patient.contact

    def getHospital(self, patient):
        return patient.hospital


# This module contains the Doctor model.
class Doctor(models.Model):
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    username = models.CharField(max_length=30, default='')
    workplace = models.ForeignKey(Hospital, null=True)

    def __str__(self):
        return self.firstName + " " + self.lastName

    def getWorkplace(self, doctor):
        return doctor.workplace


# This module contains the Nurse model.
class Nurse(models.Model):
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    username = models.CharField(max_length=30, default='')
    workplace = models.ForeignKey(Hospital, null=True)

    def __str__(self):
        return self.firstName + " " + self.lastName

    def getWorkplace(self, nurse):
        return nurse.workplace


# This module contains the Administrator model.
class Administrator(models.Model):
    firstName = models.CharField(max_length=50, default='')
    lastName = models.CharField(max_length=50, default='')
    username = models.CharField(max_length=30, default='')
    workplace = models.ForeignKey(Hospital, null=True)

    def __str__(self):
        return self.firstName + " " + self.lastName

    def getWorkplace(self, admin):
        return admin.workplace


# This module contains the Prescription model.
class Prescription(models.Model):
    name = models.CharField(max_length=50, default='')
    patient = models.ForeignKey(Patient, null=True)
    doctor = models.ForeignKey(Doctor, null=True)
    dosage = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def getPatient(self, pre):
        return pre.patient

    def getDoctor(self, pre):
        return pre.doctor


# This module contains the Test model.
class Test(models.Model):
    name = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=500)
    released = models.BooleanField(default=False)
    testResults = models.FileField(upload_to='tests', null=True, blank=True)
    patient = models.ForeignKey(Patient, null=True)
    doctor = models.ForeignKey(Doctor, null=True)

    def __str__(self):
        return self.name

    def getPatient(self, test):
        return test.patient

    def getDoctor(self, test):
        return test.doctor


# This module contains the Appointment model.
class Appointment(models.Model):
    month = models.CharField(max_length=2, default='')     # '12'
    day = models.CharField(max_length=2, default='')       # '01'
    year = models.CharField(max_length=4, default='')      # '2016'
    appttime = models.CharField(max_length=5, default='')  # '05:30'
    phase = models.CharField(max_length=2, default='')     # 'AM' or 'PM'
    patient = models.ForeignKey(Patient, null=True)
    location = models.ForeignKey(Hospital, null=True)
    doctor = models.ForeignKey(Doctor, null=True)

    def getPatient(self, appoint):
        return appoint.patient

    def getLocation(self, appoint):
        return appoint.location

    def getDoctor(self, appoint):
        return appoint.doctor


# This module contains the messaging model
class Message(models.Model):
    senderName = models.CharField(max_length=50, default='')
    senderType = models.CharField(max_length=50, default='')
    receiverName = models.CharField(max_length=50, default='')
    viewed = models.BooleanField(default=False)
    date = models.DateField(default=date.today())
    subjectLine = models.CharField(max_length=50, default='')
    message = models.TextField(max_length=500, default='')
    senderDelete = models.BooleanField(default=False)
    receiverDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.subjectLine

    def getSenderType(self, message):
        return message.senderType


# This module contains the LogInInfo model.
class LogInInfo(models.Model):
    username = models.CharField(max_length=30, default='')
    password = models.CharField(max_length=30, default='')

    def __str__(self):
        return self.username
