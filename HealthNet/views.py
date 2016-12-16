# File: views.py
# Description: This file contains Python and Django code which will form the
#              Controller element of the Model-Template-Controller (MTC) design
#              pattern.
# Author(s): Team Suites (1)

# imports
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
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
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
import datetime
from datetime import date
import os
import csv

# This variable is for storing the username entered when a user logs-in
uname = ''


# This module handles the logging of activities by saving logs to a plaintext file which is then rendered
# in HTML for administrators to view.
def logActivity(activity):
    filename = "log.txt"
    cwd = os.getcwd()
    target = open(cwd + "\\HealthNet\\log\\" + filename, 'a')
    target.write(activity)
    target.write("\n")
    target.close()


# This module handles the generic template view for the index page in which users will log-in or register
# if they have not made credentials.
class IndexView(generic.ListView):
    template_name = 'HealthNet/index.html'
    context_object_name = 'user_login_information'

    def get_queryset(self):
        return LogInInfo.objects.order_by('-username')


# This module simply renders the HTML page for the registration screen.
def registerP(request):
    return render(request, 'HealthNet/registerP.html')


# This module handles the user registration. The "LogInInfo" object is used to store their credentials in the database.
def createPLogIn(request):
    firstName = (request.POST['firstName'])
    lastName = (request.POST['lastName'])
    address = (request.POST['address'])
    number = (request.POST['number'])
    email = (request.POST['email'])
    provider = (request.POST['provider'])
    insuranceid = (request.POST['insuranceid'])
    contactfname = (request.POST['contactfname'])
    contactlname = (request.POST['contactlname'])
    contactaddress = (request.POST['contactaddress'])
    contactnumber = (request.POST['contactnumber'])
    height = (request.POST['height'])
    weight = (request.POST['weight'])
    allergies = (request.POST['allergies'])
    gender = (request.POST['gender'])
    username = (request.POST['username'])
    password = (request.POST['password'])
    try:
        logininfo = LogInInfo.objects.get(username=username)
    except ObjectDoesNotExist:
        LogInInfo.objects.create(username=username, password=password)
        global uname
        uname = username
        try:
            contact = EmergencyContact.objects.get(firstName=contactfname, lastName=contactlname,
                                                      address=contactaddress, number=contactnumber)
        except ObjectDoesNotExist:
            contact = EmergencyContact.objects.create(firstName=contactfname, lastName=contactlname,
                                                      address=contactaddress, number=contactnumber)
        Patient.objects.create(username=uname)
        patient = Patient.objects.get(username=uname)
        patient.firstName = firstName
        patient.lastName = lastName
        patient.address = address
        patient.number = number
        patient.email = email
        patient.provider = provider
        patient.insuranceid = insuranceid
        patient.contact = contact
        patient.height = height
        patient.weight = weight
        patient.allergies = allergies
        patient.gender = gender
        patient.save()

        activity = "User " + username + " registered a new account - logged on: " +\
                   datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
        logActivity(activity)
        return HttpResponseRedirect(reverse('HealthNet:home', args=()))
    else:
        return render(request, 'HealthNet/registerP.html', {
            'username': username,
            'error_message': "Username already exists.",
        })


# This module simply renders the HTML page for the password change screen.
def password(request):
    return render(request, 'HealthNet/password.html')


# This module handles the changing of a user's password
def changePass(request):
    try:
        username = (request.POST["username"])
        newpass = (request.POST["password"])
        currinfo = LogInInfo.objects.get(username=username)
    except LogInInfo.DoesNotExist:
        return render(request, 'HealthNet/password.html', {
            'username': username,
            'error_message': "There was a problem with your username.",
            })
    else:
        currinfo.password = newpass
        currinfo.save()
        activity = "User " + username + " changed their password - logged on: " +\
                   datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
        logActivity(activity)
        return HttpResponseRedirect(reverse('HealthNet:index', args=()))


# This module handles the attempt of a user to log-in to their profile. If the username and password are valid,
# the user is redirected to their profile. If not, an error message is generated and the user is
# redirected to the index page.
def verify(request):
    username = (request.POST['username'])
    passwordInput = (request.POST['password'])
    try:
        current = LogInInfo.objects.get(username=username)
    except LogInInfo.DoesNotExist:
        return render(request, 'HealthNet/index.html', {
            'username': username,
            'error_message': "There was a problem with your username.",
        })
    else:
        passwordActual = current.password
        if passwordInput == passwordActual:
            global uname
            uname = username
            activity = "User " + username + " logged in - logged on: " + datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
            logActivity(activity)
            return HttpResponseRedirect(reverse('HealthNet:home', args=()))
        else:
            return render(request, 'HealthNet/index.html', {
                'username': username,
                'error_message': "There was a problem with your password.",
            })


# This module simply renders the home page for a user
def home(request):
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                try:
                    a = Administrator.objects.get(username=uname)
                except Administrator.DoesNotExist:
                    return render(request, 'HealthNet/index.html', {
                        'error_message': "An error has occurred"
                        })
                else:
                    utype = "Administrator"
                    context = {'user': a,
                               'type': utype}
                    return render(request, 'HealthNet/home.html', context)
            else:
                utype = "Nurse"
                context = {'user': n,
                           'type': utype}
                return render(request, 'HealthNet/home.html', context)
        else:
            utype = "Doctor"
            context = {'user': d,
                       'type': utype}
            return render(request, 'HealthNet/home.html', context)
    else:
        utype = "Patient"
        context = {'user': p,
                   'type': utype}
        return render(request, 'HealthNet/home.html', context)


# This module simply renders the HTML page for the doctor and nurse registration screen.
def registerDN(request):
    workplaces = Hospital.objects.order_by("-name")
    admin = Administrator.objects.get(username=uname)
    context = {'workplaces': workplaces,
               'admin': admin}
    return render(request, 'HealthNet/registerDN.html', context)


# This module handles the doctor and nurse registration. The "LogInInfo" object is used to store their credentials
# in the database.
def createDNLogIn(request):
    firstName = (request.POST['firstName'])
    lastName = (request.POST['lastName'])
    type = (request.POST['type'])
    username = (request.POST['username'])
    password = (request.POST['password'])
    admin = Administrator.objects.get(username=uname)
    try:
        logininfo = LogInInfo.objects.get(username=username)
    except ObjectDoesNotExist:
        LogInInfo.objects.create(username=username, password=password)
        if type == "Doctor":
            Doctor.objects.create(username=username, firstName=firstName, lastName=lastName)
            d = Doctor.objects.get(username=username)
            d.workplace = admin.workplace
            d.save()
            activity = "Administrator " + uname + " registered a new doctor account - logged on: " + \
                       datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
            logActivity(activity)
            return HttpResponseRedirect(reverse('HealthNet:home', args=()))
        elif type == "Nurse":
            Nurse.objects.create(username=username,  firstName=firstName, lastName=lastName)
            n = Nurse.objects.get(username=username)
            n.workplace = admin.workplace
            n.save()
            activity = "Administrator " + uname + " registered a new nurse account - logged on: " + \
                       datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
            logActivity(activity)
            return HttpResponseRedirect(reverse('HealthNet:home', args=()))
        else:
            Administrator.objects.create(username=username, firstName=firstName, lastName=lastName)
            a = Administrator.objects.get(username=username)
            a.workplace = admin.workplace
            a.save()
            activity = "Administrator " + uname + " registered a new Administrator account - logged on: " + \
                       datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
            logActivity(activity)
            return HttpResponseRedirect(reverse('HealthNet:home', args=()))
    else:
        return render(request, 'HealthNet/registerDN.html', {
            'username': username,
            'workplace': Hospital.objects.order_by("-name"),
            'error_message': "Username already exists.",
        })


# This module simply renders the HTML page for the user information screen.
def information(request):
    global uname
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'HealthNet/home.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = "Nurse"
                patients = Patient.objects.order_by("-lastName")
                patw = Patient.objects.filter(hospital=n.workplace)
                context = {'patients': patients,
                           'patw': patw,
                           'employee': n,
                           'type': utype}
                return render(request, 'HealthNet/information.html', context)
        else:
            utype = "Doctor"
            patients = Patient.objects.order_by("-lastName")
            patw = Patient.objects.filter(hospital=d.workplace)
            context = {'patients': patients,
                       'patw': patw,
                       'employee': d,
                       'type': utype}
            return render(request, 'HealthNet/information.html', context)
    else:
        utype = "Patient"
        tests = Test.objects.filter(patient=p)
        context = {'patient': p,
                   'type': utype,
                   'tests': tests}
        return render(request, 'HealthNet/information.html', context)


# This module simply renders the HTML page for the update profile screen.
def updatePro(request):
    global uname
    patient = Patient.objects.get(username=uname)
    context = {'patient': patient}
    return render(request, 'HealthNet/updatePro.html', context)


# This module handles modifying the database object for a patient's profile information after retrieving POST data from
# the form submission. After the object is updated and saved, the user is redirected to the user information screen.
def updateProInfo(request):
    firstName = (request.POST['firstName'])
    lastName = (request.POST['lastName'])
    address = (request.POST['address'])
    number = (request.POST['number'])
    email = (request.POST['email'])
    provider = (request.POST['provider'])
    insuranceid = (request.POST['insuranceid'])
    contactfname = (request.POST['contactfname'])
    contactlname = (request.POST['contactlname'])
    contactaddress = (request.POST['contactaddress'])
    contactnumber = (request.POST['contactnumber'])
    try:
        contact = EmergencyContact.objects.get(firstName=contactfname, lastName=contactlname, address=contactaddress,
                                               number=contactnumber)
    except ObjectDoesNotExist:
        contact = EmergencyContact.objects.create(firstName=contactfname, lastName=contactlname, address=contactaddress,
                                                  number=contactnumber)
    patient = Patient.objects.get(username=uname)
    patient.firstName = firstName
    patient.lastName = lastName
    patient.address = address
    patient.number = number
    patient.email = email
    patient.provider = provider
    patient.insuranceid = insuranceid
    patient.contact = contact
    patient.save()
    activity = "User " + patient.username + " updated their profile information - logged on: " +\
               datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:information', args=()))


# This module simply renders the HTML page for the update medical information screen.
def updateMed(request, pat_id):
    global uname
    patient = Patient.objects.get(id=pat_id)
    context = {'patient': patient}
    return render(request, 'HealthNet/updateMed.html', context)


# This module handles modifying the database object for a patient's medical information after retrieving POST data from
# the form submission. After the object is updated and saved, the user is redirected to the user information screen.
def updateMedInfo(request, pat_id):
    height = (request.POST['height'])
    weight = (request.POST['weight'])
    allergies = (request.POST['allergies'])
    gender = (request.POST['gender'])
    patient = Patient.objects.get(id=pat_id)
    patient.height = height
    patient.weight = weight
    patient.allergies = allergies
    patient.gender = gender
    patient.save()
    activity = "User " + uname + " updated Patient " + patient.username + "'s medical information - logged on: " +\
               datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:information', args=()))


# This module when activated, downloads the current patient's information onto their current computer in a .csv file.
def export(request):
    global uname
    patient = Patient.objects.get(username=uname)
    testResults = Test.objects.filter(patient=patient, released=True)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="PatientInfo.csv"'
    filewriter = csv.writer(response)
    filewriter.writerow(['', 'Name', 'Email', 'Address', 'Phone Number', 'Insurance ID', 'Insurance Provider'])
    filewriter.writerow(['Patient Profile Info:', patient.lastName + "," + patient.firstName, patient.email, patient.address, patient.number, patient.insuranceid, patient.provider])
    filewriter.writerow([''])
    filewriter.writerow(['', 'Name', 'Address', 'Phone Number'])
    filewriter.writerow(['Patient Emergency Contact:', patient.contact.lastName + ", " + patient.contact.firstName, patient.contact.address, patient.contact.number])
    filewriter.writerow([''])
    filewriter.writerow(['', 'Height', 'Weight', 'Allergies', 'Gender'])
    filewriter.writerow(['Patient Medical Information:', patient.height, patient.weight, patient.allergies, patient.gender])
    filewriter.writerow([''])
    filewriter.writerow(['Patient Test Information', 'Name', 'Doctor Notes', 'Doctor Name'])
    count = 1
    for test in testResults:
        filewriter.writerow(['Test ' + str(count), test.name, test.description, test.doctor])
        count += 1
    activity = "User " + patient.username + " exported their information - logged on: " +\
               datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return response


# This module handles discharging a patient from a hospital.
def discharge(request, pat_id):
    patient = Patient.objects.get(id=pat_id)
    patient.hospital = None
    patient.save()
    return HttpResponseRedirect(reverse('HealthNet:information', args=()))


# This module handles admitting a patient to a hospital.
def admission(request, pat_id, emp_id):
    patient = Patient.objects.get(id=pat_id)
    hospital = Hospital.objects.get(id=emp_id)
    patient.hospital = hospital
    patient.save()
    return HttpResponseRedirect(reverse('HealthNet:information', args=()))


# This module handles transferring a patient from one hospital to another.
def transfer(request, pat_id, emp_id):
    patient = Patient.objects.get(id=pat_id)
    hospital = Hospital.objects.get(id=emp_id)
    patient.hospital = hospital
    patient.save()
    return HttpResponseRedirect(reverse('HealthNet:information', args=()))


# This module simply renders the HTML page for the Tests screen.
def tests(request, pat_id):
    p = Patient.objects.get(id=pat_id)
    t = Test.objects.filter(patient=p)
    context = {'patient': p,
               'test': t}
    return render(request, 'HealthNet/tests.html', context)


# This module simply renders the HTML page for the Create Test screen
def createTest(request, pat_id):
    global uname
    patient = Patient.objects.get(id=pat_id)
    context = {'patient': patient}
    return render(request, 'HealthNet/createTest.html', context)


# This module handles creating a database object for a test after retrieving POST data from the form submission.
# After the object is created and saved, the user is redirected to the main Tests screen.
def createTestInfo(request, pat_id):
    global uname
    name = (request.POST['name'])
    t = Test.objects.create()
    description = (request.POST['description'])
    try:
        if request.FILES['file']:
            file = request.FILES['file']
    except MultiValueDictKeyError:
        placeholder = ""
        t.testResults = placeholder
    else:
        t.testResults = file
    patient = Patient.objects.get(id=pat_id)
    doctor = Doctor.objects.get(username=uname)
    t.name = name
    t.description = description

    t.doctor = doctor
    t.patient = patient
    t.save()
    activity = "Doctor " + doctor.username + " created a new test for Patient " + patient.username + " - logged on: " +\
               datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:tests', args=pat_id))


# This module handles releasing a previously unreleased test for a patient. Afterwards, the user is redirected
# to the main Tests page
def releaseTest(request, test_id):
    t = Test.objects.get(id=test_id)
    t.released = True
    t.save()
    activity = "Patient " + t.patient.username + "'s test results were released by Doctor " + t.doctor.username +\
               " - logged on: " + datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:tests', args=(t.patient.id,)))


# This module simply renders the HTML page for patients to view the details of a released test
def testDetails(request, test_id):
    global uname
    test = Test.objects.get(id=test_id)
    context = {'test': test}
    return render(request, 'HealthNet/testDetails.html', context)


# This module simply renders the HTML page for the appointments screen.
def appointments(request):
    global uname
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n= Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'HealthNet/home.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = "Nurse"
                # Nurses can create and update an appointment with a Doctor at the location they work.
                # Nurses cannot cancel appointments.
                appointments = Appointment.objects.filter(location=n.workplace)
                context = {'appointments': appointments,
                           'employee': n,
                           'type': utype}
                return render(request, 'HealthNet/appointments.html', context)
        else:
            utype = "Doctor"
            # Doctors can create and update an appointment with a Doctor at a location they work.
            # Doctors can cancel THEIR appointments.
            appointments = Appointment.objects.filter(location=d.workplace)
            this_appointments = Appointment.objects.filter(doctor=d)
            context = {'appointments': appointments,
                       'this_appointments': this_appointments,
                       'employee': d,
                       'type': utype}
            return render(request, 'HealthNet/appointments.html', context)
    else:
        utype = "Patient"
        # Patients can create an appointment with any Doctor
        # Patients can update THEIR appointments
        # Patients can cancel THEIR appointments
        appointments = Appointment.objects.filter(patient=p)
        context = {'appointments': appointments,
                   'user': p,
                   'type': utype}
        return render(request, 'HealthNet/appointments.html', context)


# This module simply renders the HTML page for the create appointment screen.
def createAppt(request):
    global uname
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'HealthNet/home.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = "Nurse"
                # Nurses can create an appointment with any patient and any Doctor from their workplace.
                patients = Patient.objects.order_by("-lastName")
                doctors = Doctor.objects.filter(workplace=n.workplace)
                context = {'patients': patients,
                           'doctors': doctors,
                           'type': utype}
                return render(request, 'HealthNet/createAppt.html', context)
        else:
            utype = "Doctor"
            # Doctors can create an appointment with any patient with themselves.
            patients = Patient.objects.order_by("-lastName")
            context = {'patients': patients,
                       'doctor': d,
                       'type': utype}
            return render(request, 'HealthNet/createAppt.html', context)
    else:
        utype = "Patient"
        # Patients can create an appointment with any Doctor
        doctors = Doctor.objects.order_by("-lastName")
        context = {'patient': p,
                   'doctors': doctors,
                   'type': utype}
        return render(request, 'HealthNet/createAppt.html', context)


# This module handles creating a database object for an appointment after retrieving POST data from the form submission.
# After the object is created and saved, the user is redirected to the appointments screen.
def createApptInfo(request):
    patient = Patient.objects.get(id=(request.POST['patient']))
    doctor = Doctor.objects.get(id=(request.POST['doctor']))
    month = (request.POST['month'])
    day = (request.POST['day'])
    year = (request.POST['year'])
    appttime = (request.POST['appttime'])
    phase = (request.POST['phase'])
    location = doctor.workplace
    try:
        appointment = Appointment.objects.get(appttime=appttime, doctor=doctor, month=month, day=day, year=year, phase=phase)
    except Appointment.DoesNotExist:
        hp = Appointment.objects.create()
        hp.patient = patient
        hp.doctor = doctor
        hp.month = month
        hp.day = day
        hp.year = year
        hp.appttime = appttime
        hp.phase = phase
        hp.location = location
        hp.save()
        activity = "User " + uname + " created an appointment @ " + location.name + " on " + month + "." + day + "." +\
                    year + "," + appttime + " " + phase + " - logged on: " + datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
        logActivity(activity)
        return HttpResponseRedirect(reverse('HealthNet:appointments', args=()))
    else:
        try:
            p = Patient.objects.get(username=uname)
        except Patient.DoesNotExist:
            try:
                d = Doctor.objects.get(username=uname)
            except Doctor.DoesNotExist:
                try:
                    n = Nurse.objects.get(username=uname)
                except Nurse.DoesNotExist:
                    return render(request, 'HealthNet/home.html', {
                        'error_message': "An error has occurred"
                    })
                else:
                    utype = "Nurse"
                    # Nurses can create an appointment with any patient and any Doctor from their workplace.
                    patients = Patient.objects.order_by("-lastName")
                    doctors = Doctor.objects.filter(workplace=n.workplace)
                    context = {'patients': patients,
                               'doctors': doctors,
                               'type': utype,
                               'error_message': "The appointment could not be created, the doctor is busy at that time."}
                    return render(request, 'HealthNet/createAppt.html', context)
            else:
                utype = "Doctor"
                # Doctors can create an appointment with any patient with themselves.
                patients = Patient.objects.order_by("-lastName")
                context = {'patients': patients,
                           'doctor': d,
                           'type': utype,
                           'error_message': "The appointment could not be created, the doctor is busy at that time."}
                return render(request, 'HealthNet/createAppt.html', context)
        else:
            utype = "Patient"
            # Patients can create an appointment with any Doctor
            doctors = Doctor.objects.order_by("-lastName")
            context = {'patient': p,
                       'doctors': doctors,
                       'type': utype,
                       'error_message': "The appointment could not be created, the doctor is busy at that time."}
            return render(request, 'HealthNet/createAppt.html', context)


# This module simply renders the HTML page for the update appointment screen.
def updateAppt(request, appt_id):
    global uname
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'HealthNet/home.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = "Nurse"
                # Nurses can update an appointment to be with any Doctor from their workplace
                appointment = Appointment.objects.get(id=appt_id)
                patient = appointment.patient
                doctors = Doctor.objects.filter(workplace=n.workplace)
                context = {'appointment': appointment,
                           'patient': patient,
                           'doctors': doctors,
                           'type': utype}
                return render(request, 'HealthNet/updateAppt.html', context)
        else:
            utype = "Doctor"
            # Doctors can update an appointment to be with any Doctor from their workplace
            appointment = Appointment.objects.get(id=appt_id)
            patient = appointment.patient
            doctors = Doctor.objects.filter(workplace=d.workplace)
            context = {'appointment': appointment,
                       'patient': patient,
                       'doctors': doctors,
                       'type': utype}
            return render(request, 'HealthNet/updateAppt.html', context)
    else:
        utype = "Patient"
        # Patients can update an appointment to be with any Doctor
        appointment = Appointment.objects.get(id=appt_id)
        doctors = Doctor.objects.order_by("-lastName")
        context = {'appointment': appointment,
                   'patient': p,
                   'doctors': doctors,
                   'type': utype}
        return render(request, 'HealthNet/updateAppt.html', context)


# This module handles modifying the database object for an appointment after retrieving POST data from the form
# submission. After the object is updated and saved, the user is redirected to their appointments screen.
def updateApptInfo(request, appt_id):
    doctor = Doctor.objects.get(id=(request.POST['doctor']))
    month = (request.POST['month'])
    day = (request.POST['day'])
    year = (request.POST['year'])
    appttime = (request.POST['appttime'])
    phase = (request.POST['phase'])
    location = doctor.workplace
    try:
        appointment = Appointment.objects.get(appttime=appttime, doctor=doctor, month=month, day=day, year=year, phase=phase)
    except Appointment.DoesNotExist:
        appt = Appointment.objects.get(id=appt_id)
        appt.doctor = doctor
        appt.month = month
        appt.day = day
        appt.year = year
        appt.appttime = appttime
        appt.phase = phase
        appt.location = location
        appt.save()
        activity = "User " + uname + " updated Appointment #" + appt_id + " - logged on: " + \
                   datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
        logActivity(activity)
        return HttpResponseRedirect(reverse('HealthNet:appointments', args=()))
    else:
        try:
            p = Patient.objects.get(username=uname)
        except Patient.DoesNotExist:
            try:
                d = Doctor.objects.get(username=uname)
            except Doctor.DoesNotExist:
                try:
                    n = Nurse.objects.get(username=uname)
                except Nurse.DoesNotExist:
                    return render(request, 'HealthNet/home.html', {
                        'error_message': "An error has occurred"
                    })
                else:
                    utype = "Nurse"
                    # Nurses can update an appointment to be with any Doctor from their workplace
                    appointment = Appointment.objects.get(id=appt_id)
                    patient = appointment.patient
                    doctors = Doctor.objects.filter(workplace=n.workplace)
                    context = {'appointment': appointment,
                               'patient': patient,
                               'doctors': doctors,
                               'type': utype,
                               'error_message': "The appointment could not be created, the doctor is busy at that time."}
                    return render(request, 'HealthNet/updateAppt.html', context)
            else:
                utype = "Doctor"
                # Doctors can update an appointment to be with any Doctor from their workplace
                appointment = Appointment.objects.get(id=appt_id)
                patient = appointment.patient
                doctors = Doctor.objects.filter(workplace=d.workplace)
                context = {'appointment': appointment,
                           'patient': patient,
                           'doctors': doctors,
                           'type': utype,
                           'error_message': "The appointment could not be created, the doctor is busy at that time."}
                return render(request, 'HealthNet/updateAppt.html', context)
        else:
            utype = "Patient"
            # Patients can update an appointment to be with any Doctor
            appointment = Appointment.objects.get(id=appt_id)
            doctors = Doctor.objects.order_by("-lastName")
            context = {'appointment': appointment,
                       'patient': p,
                       'doctors': doctors,
                       'type': utype,
                       'error_message': "The appointment could not be created, the doctor is busy at that time."}
            return render(request, 'HealthNet/updateAppt.html', context)


# This module handles deleting the database object for an appointment. Afterwards, the user is redirected to
# their appointments screen.
def cancelAppt(request, appt_id):
    Appointment.objects.get(id=appt_id).delete()
    activity = "User " + uname + " cancelled Appointment #" + appt_id + " - logged on: " +\
               datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:appointments', args=()))


# This module simply loads the HTML page for the prescriptions screen.
def prescriptions(request):
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'HealthNet/home.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = "Nurse"
                pres = Prescription.objects.filter(patient__hospital = n.workplace)
                context = {'prescriptions': pres,
                           'type': utype,
                           'employee': n}
                return render(request, 'HealthNet/prescriptions.html', context)
        else:
            pres = Prescription.objects.filter(doctor=d)
            presatw = Prescription.objects.filter(patient__hospital=d.workplace)
            utype = "Doctor"
            context = {'prescriptions': pres,
                       'presatw': presatw,
                       'type': utype,
                       'employee': d}
            return render(request, 'HealthNet/prescriptions.html', context)
    else:
        utype = "Patient"
        pres = Prescription.objects.filter(patient=p)
        context = {'prescriptions': pres,
                   'type': utype,
                   'patient': p}
        return render(request, 'HealthNet/prescriptions.html', context)


# This module simply renders the HTML page for the create prescription screen.
def createPres(request):
    patients = Patient.objects.order_by("-lastName")
    context = {'patients': patients}
    return render(request, 'HealthNet/createPres.html', context)


# This module handles creating a database object for a prescription after retrieving POST data from the form submission.
#  After the object is created and saved, the user is redirected to the prescriptions screen.
def createPresInfo(request):
    global uname
    name = (request.POST['name'])
    dosage = (request.POST['dosage'])
    patient = Patient.objects.get(id=(request.POST['patient']))
    doctor = Doctor.objects.get(username=uname)
    pre = Prescription.objects.create()
    pre.name = name
    pre.dosage = dosage
    pre.doctor = doctor
    pre.patient = patient
    pre.save()
    activity = "Doctor " + doctor.username + " created a prescription for Patient " + patient.username +\
               " - logged on: " + datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:prescriptions', args=()))


# This module simply renders the HTML page for the update prescriptions screen.
def updatePres(request, pres_id):
    p = Prescription.objects.get(id=pres_id)
    patients = Patient.objects.order_by("-lastName")
    context = {'patients': patients,
               'prescription': p}
    return render(request, 'HealthNet/updatePres.html', context)


# This module handles modifying the database object after retrieving POST data from the form submission.
# After the object is updated and saved, the doctor is redirected to their prescriptions screen.
def updatePresInfo(request, pres_id):
    name = (request.POST['name'])
    dosage = (request.POST['dosage'])
    patient = Patient.objects.get(id=(request.POST['patient']))
    doctor = Doctor.objects.get(username=uname)
    pre = Prescription.objects.get(id=pres_id)
    pre.name = name
    pre.dosage = dosage
    pre.doctor = doctor
    pre.patient = patient
    pre.save()
    activity = "Doctor " + doctor.username + " updated Prescription #" + pres_id + " for Patient " + patient.username +\
               " - logged on: " + datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:prescriptions', args=()))


# This module handles deleting the database object for a prescription. Afterwards, the doctor is redirected to
# their prescriptions screen.
def removePres(request, pres_id):
    Prescription.objects.get(id=pres_id).delete()
    activity = "Doctor " + uname + " removed Prescription #" + pres_id + " - logged on: " +\
               datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:prescriptions', args=()))


# This module simply renders the HTML page for the calendar screen.
def calendar(request):
    global uname
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                return render(request, 'HealthNet/home.html', {
                    'error_message': "An error has occurred"
                })
            else:
                utype = "Nurse"
                # Nurses can view all appointments for the day and week between patients and doctors, in their workplace
                appts = Appointment.objects.filter(location=n.workplace)
                context = {'appointments': appts,
                           'user': n,
                           'type': utype}
                return render(request, 'HealthNet/calendar.html', context)
        else:
            utype = "Doctor"
            # Doctors can view all of their appointments on the calendar
            appts = Appointment.objects.filter(doctor=d)
            context = {'appointments': appts,
                           'user': d,
                           'type': utype}
            return render(request, 'HealthNet/calendar.html', context)
    else:
        utype = "Patient"
        # Patients can view all of their appointments on the calendar
        appts = Appointment.objects.filter(patient=p)
        context = {'appointments': appts,
                           'user': p,
                           'type': utype}
        return render(request, 'HealthNet/calendar.html', context)


# This module simply renders the activity log for an administrator account
def log(request):
    filename = "log.txt"
    cwd = os.getcwd()
    target = open(cwd + "\\HealthNet\\log\\" + filename, 'r')
    appString = target.readline()
    logString = []
    while appString != "":
        logString.append(appString)
        appString = target.readline()
    target.close()
    context = {'logString': logString}
    return render(request, 'HealthNet/log.html', context)


# This module simply renders the statistics page for an administrator account
def statistics(request):
    admins = Administrator.objects.count()
    doctors = Doctor.objects.count()
    nurses = Nurse.objects.count()
    patients = Patient.objects.count()
    appts = Appointment.objects.count()
    pres = Prescription.objects.count()
    context = {'admins': admins,
               'doctors': doctors,
               'nurses': nurses,
               'patients': patients,
               'appointments': appts,
               'prescriptions': pres}
    return render(request, 'HealthNet/statistics.html', context)


# This module simply renders the main messaging page for a user. All of their received and sent message are displayed
# on the page, with various options for the user to choose from.
def messages(request):
    global uname
    try:
        m = Message.objects.filter(receiverDelete=False)
        mess = m.filter(receiverName=uname)
    except Message.DoesNotExist:
        mess = Null
    try:
        sm = Message.objects.filter(senderDelete=False)
        sendmess = sm.filter(senderName=uname)
    except Message.DoesNotExist:
        sendmess = Null
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                utype = "Administrator"
            else:
                utype = "Nurse"
        else:
            utype = "Doctor"
    else:
        utype = "Patient"
    context = {'messages': mess,
               'type': utype,
               'sendMessages': sendmess}
    return render(request, 'HealthNet/messages.html', context)


# This module simply renders the create message page for a user.
def createMess(request):
    global uname
    logins = LogInInfo.objects.all()
    context = {'logins': logins}
    return render(request, 'HealthNet/createMess.html', context)


# This module simply renders the reply message page for a user.
def replyMess(request, mess_id):
    global uname
    logins = LogInInfo.objects.all()
    context = {'logins': logins,
               'message': Message.objects.get(id=mess_id)}
    return render(request, 'HealthNet/replyMess.html', context)


# This module handles creating a database object for a message after retrieving POST data from the form submission.
# After the object is created and saved, the user is redirected to the main messages page.
def createMessInfo(request, mess_id):
    global uname
    subject = (request.POST['subject'])
    description = (request.POST['message'])
    m = Message.objects.create()
    if mess_id != "-1":
        replyMess = Message.objects.get(id=mess_id)
        if replyMess.senderName == uname:
            m.receiverName = replyMess.receiverName
            m.subjectLine = "RE - " + subject
        else:
            m.receiverName = replyMess.senderName
            m.subjectLine = "RE - " + subject
    else:
        username = LogInInfo.objects.get(id=(request.POST['users'])).username
        m.receiverName = username
        m.subjectLine = subject
    try:
        p = Patient.objects.get(username=uname)
    except Patient.DoesNotExist:
        try:
            d = Doctor.objects.get(username=uname)
        except Doctor.DoesNotExist:
            try:
                n = Nurse.objects.get(username=uname)
            except Nurse.DoesNotExist:
                try:
                    a = Administrator.objects.get(username=uname)
                except Administrator.DoesNotExist:
                    return render(request, 'HealthNet/home.html', {
                        'error_message': "An error has occurred"
                        })
                else:
                    utype = "Administrator"
            else:
                utype = "Nurse"
        else:
            utype = "Doctor"
    else:
        utype = "Patient"
    m.senderName = uname
    m.senderType = utype
    m.date = date.today()
    m.message = description
    m.save()
    activity = utype + " " + uname + " sent a message to " + m.receiverName + " - logged on: " + \
               datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return messages(request)


# This module simply displays the View Message page for a user when they select the option to view a received/sent
# message.
def viewMess(request, mess_id):
    global uname
    mess = Message.objects.get(id=mess_id)
    context = {'message': mess}
    return render(request, 'HealthNet/viewMess.html', context)


# This module handles deleting a preexisting message from a user's inbox.
def deleteMess(request, mess_id):
    global uname
    mess = Message.objects.get(id=mess_id)
    if uname == mess.senderName:
        mess.senderDelete = True
        mess.save()
    else:
        mess.receiverDelete = True
        mess.save()

    if mess.senderDelete is True and mess.receiverDelete is True:
        mess.delete()

    activity = uname + " deleted message# " + mess_id + " - logged on: " + \
               datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:messages', args=()))


# This module handles logging-out a user. Afterwards the user is redirected to the index screen.
def logOut(request):
    global uname
    activity = "User " + uname + " logged out - logged on: " + datetime.datetime.now().strftime('%m/%d/%y @ %H:%M:%S')
    uname = ''
    logActivity(activity)
    return HttpResponseRedirect(reverse('HealthNet:index', args=()))
