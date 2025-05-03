# from django.urls import path
# from erp.patient import views




######added myself
from django.urls import path
from erp.patient import views

app_name = "patient"  # ✅ Add this

urlpatterns = [
    path('register/', views.patient_registration, name="register"),
    path('dashboard/', views.patient_dashboard, name="dashboard"),
    path('diagnosis-history/', views.patient_diagnosis_history, name='diagnosis_history'),
]
