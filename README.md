# HealthNet

### Introduction:
* This project was created over the course of a semester for SWEN 261(Introcution to Software Engineering) at RIT. David Matz, Michael Gilmour, Derek Freeman and myself worked in a team to create this finished produyct for our customer (Professor). We were given detailed requirements and had to simultanesously build our product as well as maintain and update several documents (Design, Requirements, Project Plan, Test Tracker). We completed two releases and the code and documents for our 2nd release are held in this repository.

### Installation:  
* This web app will work on any type of machine (Windows, macOS, Linux) so long as you already have the software stack detailed by our instructor (Python 3.4.3, SQLite 3.8.3.1, Django 1.9.1).
* __Steps to run:__
	1. Unzip the file to the desired directory
	2. Navigate into the folder containing __"manage.py"__
	3. Shift-right click in the folder
	4. Click __"Open command window here"__
  5. In the command window type __"python manage.py runserver"__
  6. Press enter
  7. Open a web browser of your choice
  8. Navigate to “http://127.0.0.1:8000/HealthNet”
  9. Enjoy!

### Known Bugs and Disclaimers:
* This is a work in progress. There are bugs (Nobody is perfect!)
* If you choose to include a file when creating a Test Result for a Patient, the file is properly uploaded, but when the Patient goes to view their new Test Result and download the attached file, the file becomes corrupted and is unable to be opened.

### Basic Execution and Usage Instructions (Logins & Passwords)
1. See “Installation: Steps to run” above

2. Login with existing credentials:
 1. Enter in login information:
 
   | Username | Password | Type | Workplace |
   | ------------- |:-------------:|:-------------:| -----:|
   | admin1 | Password123! | Administrator | Hospital 1 |
   | admin2 | Password123! | Administrator | Hospital 2 |
   | patient | Password123! | Patient | None |
   | nurse1 | Password123! | Nurse | Hospital 1 |
   | nurse2 | Password123! | Nurse | Hospital 2 |
   | doctor1 | Password123! | Doctor | Hospital 1 |
   | doctor2 | Password123! | Doctor | Hospital 2 |
   
  2. Click “Log In” (If the information entered is invalid, an alert will notify you of the invalid information and ask you to resubmit)
  3. You will be redirected to the Home page

3. Register a new user
 1. Click “Register”
 2. Fill out registration form
 3. Click “Submit” (If the information entered is invalid, an alert will notify you of the invalid information and ask you to resubmit)
 4. You will be redirected to the Home page

4. From here the user can do several actions such as:
 1. Navigate to the Information page which holds all user information (Profile information (Patients only), Medical Information (Editable for Doctors and Nurses) and Tests Results)
 2. Navigate to the Appointments page where the user can create, update and cancel appointments
 3. Navigate to the Calendar page, to view future applicable appointments in a visual format
 4. Navigate to the Prescriptions page, To view, delete (Doctor only), edit (Doctor only) or update (Doctor only) prescriptions.
 5. Navigate to the Messages page, to send, read, reply to and delete messages sent by users of the system
 6. Logout of HealthNet
 
* Administrators can do the following:
 1. Navigate to the System Log page where they can view the HealthNet Activity Log
 2. Navigate to the System Statistics page where they can view System Statistics
 3. Navigate to the Register Doctor/Nurse/Administrator page where they can register new doctors, administrators and nurses into the system
 4. Or Logout of HealthNet
