from django.contrib import admin

from erp.doctor.models import Doctor, Diagnosis, Prescription, Department, Staff

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Diagnosis)
admin.site.register(Prescription)
admin.site.register(Staff)
admin.site.register(Department)
