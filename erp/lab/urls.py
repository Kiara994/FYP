from django.urls import path
from erp.lab import views


app_name = "lab"  # ✅ Add this

urlpatterns = [

    path('create_lab_test/', views.create_lab_test, name="labtest"),
path('labtest/<int:labtest_id>/', views.update_labtest_result, name='update_labtest_result'),



]
