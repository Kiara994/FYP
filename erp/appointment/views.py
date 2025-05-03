from datetime import date
from gc import get_objects

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PatientAppointmentForm, DoctorAppointmentForm,RescheduleAppointmentForm
from erp.patient.views import home
from erp.patient.models import Patient
from erp.appointment.models import Appointment
from erp.doctor.models import Doctor

# Create your views here.





def patient_appointment_scheduling(request):
    """View for scheduling a patient's appointment."""

    # ✅ Ensure the user has a patient profile
    if not hasattr(request.user, "patient_profile"):
        messages.error(request, "You must be registered as a patient to schedule an appointment.")
        return redirect("account_login")

    form = PatientAppointmentForm(request.POST or None)  # ✅ Load form

    if request.method == 'POST' and form.is_valid():
        appointment = form.save(commit=False)  # ✅ Do not save yet
        appointment.patient = request.user.patient_profile  # ✅ Assign the patient

        # ✅ Check if the doctor is already booked at this time
        if Appointment.objects.filter(
            doctor=appointment.doctor,
            appointment_date=appointment.appointment_date,
            appointment_time=appointment.appointment_time
        ).exists():
            messages.error(request, "The doctor is already booked at this time. Please choose another time.")
            return render(request, "appointment/appointment_scheduling.html", {'form': form})

        # ✅ Check if the patient already has an appointment at the same time
        if Appointment.objects.filter(
            patient=appointment.patient,
            appointment_date=appointment.appointment_date,
            appointment_time=appointment.appointment_time
        ).exists():
            messages.error(request, "You already have an appointment at this time.")
            return render(request, "appointment/appointment_scheduling.html", {'form': form})

        # ✅ Save only after all checks pass
        appointment.save()

        send_appointment_email(
            user_email=appointment.patient.user.email,
            name=appointment.patient.name,
            appointment_date=f"{appointment.appointment_date} at {appointment.appointment_time}",
            role="Patient"
        )

        send_appointment_email(
            user_email=appointment.doctor.user.email,
            name=appointment.doctor.name,
            appointment_date=f"{appointment.appointment_date} at {appointment.appointment_time}",
            role="Doctor"
        )

        messages.success(request, "Appointment scheduled successfully.")
        return redirect("patient:dashboard")

    return render(request, "appointment/appointment_scheduling.html", {'form': form})



def doctor_appointment_scheduling(request):
    """View for a doctor to schedule an appointment for a patient."""

    # ✅ Ensure the user is a doctor
    if not hasattr(request.user, "doctor_profile"):
        messages.error(request, "You must be registered as a doctor to schedule an appointment.")
        return redirect("account_login")

    form = DoctorAppointmentForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        appointment = form.save(commit=False)  # ✅ Do not save yet
        appointment.doctor = request.user.doctor_profile  # ✅ Assign the logged-in doctor

        # ✅ Check if the doctor already has an appointment at the same time
        if Appointment.objects.filter(
            doctor=appointment.doctor,
            appointment_date=appointment.appointment_date,
            appointment_time=appointment.appointment_time
        ).exists():
            messages.error(request, "You already have an appointment at this time.")
            return render(request, "appointment/appointment_scheduling.html", {'form': form})

        # ✅ Check if the patient already has another appointment at the same time
        if Appointment.objects.filter(
            patient=appointment.patient,
            appointment_date=appointment.appointment_date,
            appointment_time=appointment.appointment_time
        ).exists():
            messages.error(request, "The patient already has an appointment at this time.")
            return render(request, "appointment/appointment_scheduling.html", {'form': form})

        appointment.save()  # ✅ Save only after passing all checks

        send_appointment_email(
            user_email=appointment.patient.user.email,
            name=appointment.patient.name,
            appointment_date=f"{appointment.appointment_date} at {appointment.appointment_time}",
            role="Patient"
        )

        send_appointment_email(
            user_email=appointment.doctor.user.email,
            name=appointment.doctor.name,
            appointment_date=f"{appointment.appointment_date} at {appointment.appointment_time}",
            role="Doctor"
        )

        messages.success(request, "Appointment scheduled successfully.")
        return redirect("doctor:dashboard")

    return render(request, "appointment/appointment_scheduling.html", {'form': form})


def patient_appointment(request,patient_id):
    patient=get_object_or_404(Patient,id=patient_id)
    appointments=Appointment.objects.filter(patient=patient)
    return render(request,"appointment/patient_appointment_page.html",{'patient':patient,'appointments':appointments})



def doctor_appointment(request,doctor_id):
    doctor=get_object_or_404(Doctor,id=doctor_id)
    today = date.today()
    appointments = Appointment.objects.filter(
        doctor=doctor,
         # Only show future and today's appointments
    )
    return render(request,"appointment/doctor_appointment_page.html",{'doctor':doctor,'appointments':appointments})




def delete_appointment_patient(request,appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.patient_profile)
    appointment.delete()
    return redirect("patient:dashboard")  # Redirect back to dashboard

def delete_appointment_doctor(request,appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=request.user.doctor_profile)
    # appointment.status = "Cancelled"
    appointment.delete()
    return redirect("doctor:dashboard")  # Redirect back to dashboard




@login_required
def reschedule_appointment_patient(request, appointment_id):
    """Allow a patient to reschedule their own appointment."""

    # ✅ Ensure the user has a patient profile
    if not hasattr(request.user, "patient_profile"):
        messages.error(request, "You must be registered as a patient to reschedule an appointment.")
        return redirect("account_login")

    # ✅ Get the patient's appointment
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.patient_profile)

    if request.method == "POST":
        form = RescheduleAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            new_appointment = form.save(commit=False)
            new_appointment.status = "Rescheduled"

            # ✅ Check if the doctor already has an appointment at the same time
            if Appointment.objects.filter(
                doctor=new_appointment.doctor,
                appointment_date=new_appointment.appointment_date,
                appointment_time=new_appointment.appointment_time
            ).exclude(id=new_appointment.id).exists():
                messages.error(request, "The doctor is already booked at this time. Please choose another time.")
                return render(request, "appointment/appointment_scheduling.html", {"form": form, "appointment": appointment})

            # ✅ Check if the patient already has another appointment at the same time
            if Appointment.objects.filter(
                patient=new_appointment.patient,
                appointment_date=new_appointment.appointment_date,
                appointment_time=new_appointment.appointment_time
            ).exclude(id=new_appointment.id).exists():
                messages.error(request, "You already have an appointment at this time.")
                return render(request, "appointment/appointment_scheduling.html", {"form": form, "appointment": appointment})

            new_appointment.save()  # ✅ Save only after passing all checks
            messages.success(request, "Appointment rescheduled successfully.")
            return redirect("patient:dashboard")  # Redirect after rescheduling

    else:
        form = RescheduleAppointmentForm(instance=appointment)

    return render(request, "appointment/appointment_scheduling.html", {"form": form, "appointment": appointment})




############## APOINTMENT NOTIFICATION      ################

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_appointment_email(user_email, name, appointment_date, role):
    subject = f"Upcoming Appointment Reminder for {name}"

    context = {
        'name': name,
        'appointment_date': appointment_date,
        'role': role
    }

    html_message = render_to_string("emails/appointment_notification.html", context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        'no-reply@hospitexerp.com',
        [user_email],
        html_message=html_message,
    )
