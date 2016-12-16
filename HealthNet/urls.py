# File: urls.py
# Description: This file contains the Django url statements.
# Author(s): Team Suites (1)

# imports
from django.conf.urls import url
from . import views

# url statements
app_name = 'HealthNet'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^register/$', views.registerP, name='registerP'),
    url(r'^register/create$', views.createPLogIn, name='createPLogIn'),
    url(r'^password/$', views.password, name='password'),
    url(r'^password/changepass/$', views.changePass, name='changepass'),
    url(r'^verify/$', views.verify, name='verify'),
    url(r'^home/$', views.home, name='home'),
    url(r'^home/registerDN$', views.registerDN, name='registerDN'),
    url(r'^home/registerDN/createDN$', views.createDNLogIn, name='createDNLogIn'),
    url(r'^information/$', views.information, name='information'),
    url(r'^information/updatePro$', views.updatePro, name='updatePro'),
    url(r'^information/updatePro/updateProInfo$', views.updateProInfo, name='updateProInfo'),
    url(r'^information/updateMed/(?P<pat_id>[0-9]+)/', views.updateMed, name='updateMed'),
    url(r'^information/updateMed/updateMedInfo/(?P<pat_id>[0-9]+)/', views.updateMedInfo, name='updateMedInfo'),
    url(r'^information/export$', views.export, name='export'),
    url(r'^information/tests/(?P<pat_id>[0-9]+)/', views.tests, name='tests'),
    url(r'^information/tests/createTest/(?P<pat_id>[0-9]+)/', views.createTest, name='createTest'),
    url(r'^information/tests/createTest/createTestInfo/(?P<pat_id>[0-9]+)/', views.createTestInfo, name='createTestInfo'),
    url(r'^information/tests/releaseTest/(?P<test_id>[0-9]+)/', views.releaseTest, name='releaseTest'),
    url(r'^information/testDetails/(?P<test_id>[0-9]+)/', views.testDetails, name='testDetails'),
    url(r'^information/discharge/(?P<pat_id>[0-9]+)/', views.discharge, name='discharge'),
    url(r'^information/admission/(?P<pat_id>[0-9]+)/(?P<emp_id>[0-9]+)/', views.admission, name='admission'),
    url(r'^information/transfer/(?P<pat_id>[0-9]+)/(?P<emp_id>[0-9]+)/', views.transfer, name='transfer'),
    url(r'^appointments/$', views.appointments, name='appointments'),
    url(r'^appointments/createAppt$', views.createAppt, name='createAppt'),
    url(r'^appointments/createAppt/createApptInfo$', views.createApptInfo, name="createApptInfo"),
    url(r'^appointments/updateAppt/(?P<appt_id>[0-9]+)/', views.updateAppt, name='updateAppt'),
    url(r'^appointments/updateAppt/updateApptInfo/(?P<appt_id>[0-9]+)/', views.updateApptInfo, name='updateApptInfo'),
    url(r'^appointments/cancelAppt/(?P<appt_id>[0-9]+)/', views.cancelAppt, name='cancelAppt'),
    url(r'^prescriptions/$', views.prescriptions, name='prescriptions'),
    url(r'^prescriptions/createPres$', views.createPres, name='createPres'),
    url(r'^prescriptions/createPres/createPresInfo$', views.createPresInfo, name="createPresInfo"),
    url(r'^prescriptions/updatePres/(?P<pres_id>[0-9]+)/', views.updatePres, name='updatePres'),
    url(r'^prescriptions/updatePres/updatePresInfo/(?P<pres_id>[0-9]+)/', views.updatePresInfo, name='updatePresInfo'),
    url(r'^prescriptions/removePres/(?P<pres_id>[0-9]+)/', views.removePres, name='removePres'),
    url(r'^calendar/$', views.calendar, name='calendar'),
    url(r'^messages/$', views.messages, name='messages'),
    url(r'^messages/createMess/$', views.createMess, name='createMess'),
    url(r'^messages/createMess/createMessInfo/(?P<mess_id>-1)/', views.createMessInfo, name="createMessInfo"),
    url(r'^messages/replyMess/(?P<mess_id>[0-9]+)/', views.replyMess, name='replyMess'),
    url(r'^messages/replyMess/createMessInfo/(?P<mess_id>[0-9]+)/', views.createMessInfo, name="createMessInfo"),
    url(r'^messages/viewMess/(?P<mess_id>[0-9]+)/', views.viewMess, name='viewMess'),
    url(r'^messages/deleteMess/(?P<mess_id>[0-9]+)/', views.deleteMess, name='deleteMess'),
    url(r'^log/$', views.log, name='log'),
    url(r'^statistics/$', views.statistics, name='statistics'),
    url(r'^logOut/$', views.logOut, name='logOut')
]
