from django.urls import path
from erp.billing import views

app_name="billing"
urlpatterns=[
    path("bill/",views.billing_creation,name="bill"),
    path("patient/<int:patient_id>/bills/", views.patient_billing, name="patient_billing"),
    path("pay/<int:bill_id>/", views.pay_bill, name="pay_bill"),


]
