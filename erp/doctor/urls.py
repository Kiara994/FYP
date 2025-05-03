

############ adde dmyseld

from django.urls import path
from erp.doctor import views
from erp.doctor.views import prescribe_prescription

app_name = "doctor"  # ✅ Add this

urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name="dashboard"),  # ✅ Use just "dashboard"
    path('register/', views.doctor_registration, name="register"),
    path("staff_register/", views.staff_registration, name="staff_register"),
    path("staff_dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path("prescribe_prescription/<int:doctor_id>/",views.prescribe_prescription,name="prescribe_prescription"),
    path("diagnosis/<int:doctor_id>/",views.doctor_diagnosis,name="doctor_diagnosis"),
    # path("ai_predict/", views.ai_predict_view, name="ai_predict"),  # AI prediction API
    path("diagnosis/edit/<int:diagnosis_id>/", views.edit_diagnosis, name="edit_diagnosis"),

    # autofill   age and gender
    path('get-patient-info/', views.get_patient_info, name='get_patient_info'),



]
