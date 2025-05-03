from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from erp.appointment.models import Appointment
from erp.lab.forms import CreateLabTestForm, LabTestResultForm
from erp.lab.models import LabTest


# Create your views here.


# def create_lab_test(request):
#     if not hasattr(request.user, 'staff_profile'):
#         return redirect("account_login")  # Only staff can access
#     form=CreateLabTestForm()
#     if request.method == "POST":
#         form = CreateLabTestForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("doctor:dashboard")  # Redirect to staff dashboard
#
#
#
#     return render(request, "lab/create_lab_test.html", {"form":form})

###### create labtest by checking time of test and appointment
# def create_lab_test(request):
#     if not hasattr(request.user, 'staff_profile'):
#         return redirect("account_login")  # Only staff can access
#
#     form = CreateLabTestForm()
#
#
#
#     if request.method == 'POST' and form.is_valid():
#             # Retrieve the patient and test date from the form data
#             new_test = form.save(commit=False)
#             # patient = form.cleaned_data['patient']
#             # test_date = form.cleaned_data['test_date']
#
#             # Check if the patient has any appointments at the same time
#             conflicting_appointments = Appointment.objects.filter(
#                 patient=new_test.patient,
#                 appointment_date=new_test.test_date,  # Check if appointment date matches
#                 appointment_time=new_test.test_date  # Check if appointment time matches
#             )
#
#             # Check if the patient has any lab tests at the same time
#             conflicting_lab_tests = LabTest.objects.filter(
#                 patient=new_test.patient,
#                 test_date=new_test.test_date,
#                 test_time=new_test.test_time,
#             )
#
#             if conflicting_appointments.exists() or conflicting_lab_tests.exists():
#                 # If there are conflicts, show a message to the staff and prevent saving
#                 messages.error(request, "This patient already has an appointment or lab test at this time.")
#                 return render(request, "lab/create_lab_test.html", {"form": form})
#
#             # If no conflicts, save the lab test
#             form.save()
#             messages.success(request, "Lab test created successfully.")
#             return redirect("doctor:staff_dashboard")  # Redirect to staff dashboard
#
#     return render(request, "lab/create_lab_test.html", {"form": form})














from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateLabTestForm
from .. import patient


def create_lab_test(request):
    if not hasattr(request.user, 'staff_profile'):
        return redirect("account_login")  # Only staff can access

    if request.method == 'POST':
        form = CreateLabTestForm(request.POST)  # ✅ Bind the form with POST data
        if form.is_valid():
            new_test = form.save(commit=False)
            new_test.technician = request.user.staff_profile

            # Extract the date and time properly
            test_date = new_test.test_date.date()
            test_time = new_test.test_time

            # # Check for conflicting appointments
            # conflicting_appointments = Appointment.objects.filter(
            #     patient=new_test.patient,
            #     appointment_date=test_date,
            #     appointment_time=test_time
            # )
            #
            #
            #
            #
            # # Check for conflicting lab tests
            # conflicting_lab_tests = LabTest.objects.filter(
            #     patient=new_test.patient,
            #     test_date__date=test_date,  # Compare just the date part of test_date
            #     test_time=test_time
            # )
            #
            # if conflicting_appointments.exists() or conflicting_lab_tests.exists():
            #     messages.error(request, "This patient already has an appointment or lab test at this time.")
            #     return render(request, "lab/create_lab_test.html", {"form": form})

            if Appointment.objects.filter(
                patient=new_test.patient,
                appointment_date=test_date,
                appointment_time=test_time
            ).exists():
                messages.error(request, "This patient already has an appointment at this time.")
                return render(request, "lab/create_lab_test.html", {"form": form})


            if LabTest.objects.filter(
                patient=new_test.patient,
                test_date__date=test_date,  # Compare just the date part of test_date
                test_time=test_time
            ).exists():
                messages.error(request, "This patient already has a lab test at this time.")
                return render(request, "lab/create_lab_test.html", {"form": form})



            # Save only after all checks
            new_test.save()
            send_labtest_email(
                user_email=new_test.patient.user.email,
                name=new_test.patient.name,
                test_name=new_test.test_name,
                test_date=new_test.test_date
            )
            messages.success(request, "Lab test created successfully.")
            return redirect("doctor:staff_dashboard")
        else:
            messages.error(request, "Invalid form data. Please correct the errors.")
    else:
        form = CreateLabTestForm()

    return render(request, "lab/create_lab_test.html", {"form": form})







########################     LABTEST RESULT UPDATE    #################
# views.py
@login_required
def update_labtest_result(request, labtest_id):
    if not hasattr(request.user, 'staff_profile') or request.user.staff_profile.role != 'Technician':
        return redirect('account_login')

    technician = request.user.staff_profile
    lab_test = get_object_or_404(LabTest, id=labtest_id, technician=technician, status='completed')

    if request.method == 'POST':
        form = LabTestResultForm(request.POST, instance=lab_test)
        if form.is_valid():
            form.save()
            return redirect('doctor:staff_dashboard')
    else:
        form = LabTestResultForm(instance=lab_test)

    return render(request, 'lab/update_labtest_result.html', {
        'form': form,
        'lab_test': lab_test,
    })




########################     LABTEST NOTIFICATION    #################



def send_labtest_email(user_email, name, test_name, test_date):
    subject = f"Lab Test Scheduled: {test_name}"

    context = {
        'name': name,
        'test_name': test_name,
        'test_date': test_date
    }

    html_message = render_to_string("emails/labtest_notification.html", context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,

        'no-reply@hospitexerp.com',
        [user_email],
        html_message=html_message,
    )
