from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Test
from .models import Patient
from .models import EmergencyContact
from .models import Doctor
from .models import Nurse
from .models import Prescription
from .models import Hospital
from .models import Appointment
from .models import LogInInfo
from .models import Administrator
from .models import Message


class ModelsTests(TestCase):
    #test all of the model functions
    def setUp(self):
        message = Message.objects.create(senderName = "Senders Name", senderType = "Patient")
        EC = EmergencyContact.objects.create(firstName="Emergency", lastName ="Contact", number="(575)456-1982", address="123 bb baker street")
        Hopsital = Hospital.objects.create(name = "hospital1")
        patient = Patient.objects.create(username = "Patient", hospital = Hopsital, contact = EC)
        doctor = Doctor.objects.create(username = "Doctor", workplace = Hopsital)
        nurse = Nurse.objects.create(username = "Nurse", workplace = Hopsital)
        admin = Administrator.objects.create(username = "Admin", workplace = Hopsital)
        appointment = Appointment.objects.create(appttime = "05:30", patient = patient, location = Hopsital, doctor = doctor)
        test = Test.objects.create(name = "TestingTest", doctor = doctor, patient = patient)
        pre = Prescription.objects.create(name = "TestingPrescription", doctor = doctor, patient = patient)

    def test_getMessageSenderType(self):
        message = Message.objects.get(senderName = "Senders Name")
        self.assertEqual(message.getSenderType(message), "Patient")

    def test_getPatientEC(self):
        patient = Patient.objects.get(username="Patient")
        EC = EmergencyContact.objects.get(firstName="Emergency")
        self.assertEqual(patient.getEmergencyContact(patient), EC)

    def test_getPatientHospital(self):
        patient = Patient.objects.get(username="Patient")
        hospital = Hospital.objects.get(name="hospital1")
        self.assertEqual(patient.getHospital(patient), hospital)

    def test_getApptPatient(self):
        appt = Appointment.objects.get(appttime="05:30")
        patient = Patient.objects.get(username="Patient")
        self.assertEqual(appt.getPatient(appt), patient)

    def test_getApptDoctor(self):
        doctor = Doctor.objects.get(username="Doctor")
        appt = Appointment.objects.get(appttime="05:30")
        self.assertEqual(appt.getDoctor(appt), doctor)

    def test_getApptLocation(self):
        location = Hospital.objects.get(name="hospital1")
        appt = Appointment.objects.get(appttime="05:30")
        self.assertEqual(appt.getLocation(appt), location)

    def test_getTestDoctor(self):
        doctor = Doctor.objects.get(username="Doctor")
        test = Test.objects.get(name="TestingTest")
        self.assertEqual(test.getDoctor(test), doctor)

    def test_getTestPatient(self):
        patient = Patient.objects.get(username="Patient")
        test = Test.objects.get(name="TestingTest")
        self.assertEqual(test.getPatient(test), patient)

    def test_getPrescriptionDoctor(self):
        doctor = Doctor.objects.get(username="Doctor")
        pre = Prescription.objects.get(name="TestingPrescription")
        self.assertEqual(pre.getDoctor(pre), doctor)

    def test_getPrescriptionPatient(self):
        patient = Patient.objects.get(username="Patient")
        pre = Prescription.objects.get(name="TestingPrescription")
        self.assertEqual(pre.getPatient(pre), patient)

    def test_getAdministratorWorkplace(self):
        workplace = Hospital.objects.get(name="hospital1")
        admin = Administrator.objects.get(username="Admin")
        self.assertEqual(admin.getWorkplace(admin), workplace)

    def test_getNurseWorkplace(self):
        workplace = Hospital.objects.get(name="hospital1")
        nurse = Nurse.objects.get(username="Nurse")
        self.assertEqual(nurse.getWorkplace(nurse), workplace)

    def test_getDoctorWorkplace(self):
        workplace = Hospital.objects.get(name="hospital1")
        doctor = Doctor.objects.get(username="Doctor")
        self.assertEqual(doctor.getWorkplace(doctor), workplace)

#test the functionality in the models
class ViewsTests(TestCase):
    #test all of the main pages
    def test_home(self):
        response = self.client.get(reverse('HealthNet:home'))
        self.assertEqual(response.status_code, 200)


    def test_index(self):
        response = self.client.get(reverse('HealthNet:index'))
        self.assertEqual(response.status_code, 200)


    def test_information(self):
        response = self.client.get(reverse('HealthNet:information'))
        self.assertEqual(response.status_code, 200)


    def test_appointments(self):
        response = self.client.get(reverse('HealthNet:appointments'))
        self.assertEqual(response.status_code, 200)


    def test_prescriptions(self):
        response = self.client.get(reverse('HealthNet:prescriptions'))
        self.assertEqual(response.status_code, 200)