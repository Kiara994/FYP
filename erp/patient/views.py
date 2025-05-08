from http.client import HTTPResponse

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.timezone import now

from erp.lab.models import LabTest
from erp.billing.models import Billing
from erp.appointment.models import Appointment
from erp.doctor.models import Prescription,Diagnosis

from .forms import PatientRegistrationForm
from django.shortcuts import render, redirect


# Create your views here.
def home(request):
    return HttpResponse("hallo")
#
# @login_required
# def patient_registration(request):
#     form=PatientRegistrationForm()
#     if request.method=='POST':
#         form=PatientRegistrationForm(request.POST)
#         if form.is_valid():
#             form.save(commit=True)
#             return home(request)
#     else:
#         print("error form is invalid")
#
#     return render(request,"patient/patient_registration.html",{'form':form})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PatientRegistrationForm
from .models import Patient

@login_required
def patient_registration(request):
    user = request.user  # Get the logged-in user

    # Check if the user is already registered to prevent duplicate registrations
    if user.is_registered:
        return redirect("patients:dashboard")  # Redirect to patient dashboard if already registered

    form = PatientRegistrationForm()

    if request.method == "POST":
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)  # Don't save yet
            patient.user = user  # Assign the logged-in user
            patient.save()  # Now save to database

            user.is_registered = True  # Mark user as registered
            user.save()

            return redirect("patient:dashboard")  # Redirect to patient dashboard

    return render(request, "patient/patient_registration.html", {"form": form})



# @login_required
# def patient_dashboard(request):
#
#
#     if request.user.is_authenticated and hasattr(request.user,'patient'):
#         patient=request.user.patient
#         appointments=Appointment.objects.filter(patient=patient).order_by("-appointment_date")[:5]
#         prescriptions=Prescription.objects.filter(patient=patient).order_by("-prescription_date")[:5]
#         lab_tests=LabTest.objects.filter(patient=patient).order_by("-test_date")[:5]
#         bills=Billing.objects.filter(patient=patient).order_by("-billing_date")[:5]
#         diagnosis=Diagnosis.objects.filter(patient=patient).order_by("-diagnosis_date")[:5]
#         context={
#             'patient':patient,
#             'appointments':appointments,
#             'prescriptions':prescriptions,
#             'lab_tests':lab_tests,
#             'bills':bills,
#             'diagnosis':diagnosis
#         }
#         render(request,"patient/patient_dashboard.html",context)




@login_required
def patient_dashboard(request):
    if not hasattr(request.user, 'patient_profile') or request.user.patient_profile is None:
        return redirect("account_login")  # Redirect if user has no patient profile

    patient = request.user.patient_profile  #  Use `patient_profile`
    appointments = Appointment.objects.filter(patient=patient).order_by("-appointment_date")[:5]
    prescriptions = Prescription.objects.filter(patient=patient).order_by("-prescription_date")[:5]
    lab_tests = LabTest.objects.filter(patient=patient).order_by("-test_date")[:5]
    bills = Billing.objects.filter(patient=patient).order_by("-billing_date")[:5]
    diagnosis = Diagnosis.objects.filter(patient=patient).order_by("-diagnosis_date")[:5]



    # Dynamically assign "completed" to tests in the past that are still pending
    for test in lab_tests:
        if test.status == "pending" and test.test_date < now():
            test.status = "completed"
            test.save()

        #  Update appointment status based on datetime comparison
    for appointment in appointments:
        new_status = appointment.current_status()
        if new_status != appointment.status:
            appointment.status = new_status
            appointment.save()

    context = {
        "patient": patient,  #  Ensure correct reference in template
        "appointments": appointments,
        "prescriptions": prescriptions,
        "lab_tests": lab_tests,
        "bills": bills,
        "diagnosis": diagnosis,
    }

    return render(request, "patient/patient_dashboard.html", context)  #  Use correct template



@login_required
def patient_diagnosis_history(request):
    # Get the logged-in user's patient profile
    patient_profile = request.user.patient_profile

    # Filter diagnosis records for this patient
    diagnoses = Diagnosis.objects.filter(patient=patient_profile).order_by('-diagnosis_date')

    return render(request, 'patient/patient_diagnosis.html', {'diagnoses': diagnoses})




###########################      auto age gendefr       ##########################


