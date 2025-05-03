from django.urls import path

from config.api_router import app_name
from erp.appointment import views
app_name="appointment"

urlpatterns=[
    path("schedule_appointment_patient",views.patient_appointment_scheduling,name="schedule_appointment_patient"),
    path("schedule_appointment_doctor",views.doctor_appointment_scheduling,name="schedule_appointment_doctor"),
    path("patient_appointment/<int:patient_id>/",views.patient_appointment,name="patient_appointment"),
    path("doctor_appointment/<int:doctor_id>/",views.doctor_appointment,name="doctor_appointment"),
    path("delete_appointment_patient/<int:appointment_id>",views.delete_appointment_patient,name="delete_appointment"),
    path("delete_appointment_doctor/<int:appointment_id>",views.delete_appointment_doctor,name="delete_appointment_doctor"),
    path("reschedule_appointment/<int:appointment_id>",views.reschedule_appointment_patient,name="reschedule_appointment"),

]
