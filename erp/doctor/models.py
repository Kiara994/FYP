from django.conf import settings
from django.db import models
# from phonenumber_field.modelfields import PhoneNumberField

from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),

]


class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_profile",null=True, blank=True)

    name=models.CharField(max_length=70)
    speciality=models.CharField(max_length=100)
    contact_info=PhoneNumberField(unique=True,region='PK')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    availability=models.CharField(max_length=20)
    license_number = models.CharField(max_length=20, unique=True)
    department=models.CharField(max_length=80)
    joining_date=models.DateField(auto_now_add=True)
    shift_timings = models.CharField(max_length=50)

    salary = models.DecimalField(max_digits=10, decimal_places=2,null=True)

    def __str__(self):
        return f"{self.name} ({self.license_number})"



class Diagnosis(models.Model):
    patient=models.ForeignKey('patient.Patient',on_delete=models.CASCADE)

    doctor=models.ForeignKey(Doctor,on_delete=models.SET_NULL,null=True)
    diagnosis_date=models.DateField(auto_now_add=True)
    diagnosis_detail=models.TextField(blank=True,null=True)
    tests_ordered=models.TextField(blank=True,null=True)
    symptoms=models.TextField(blank=True,null=True)
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female")], null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    blood_pressure = models.CharField(max_length=50, blank=True, null=True)
    cholesterol_level = models.CharField(max_length=50, blank=True, null=True)
    fever = models.CharField(max_length=10, choices=[("Yes", "Yes"), ("No", "No")], blank=True, null=True)
    cough = models.CharField(max_length=10, choices=[("Yes", "Yes"), ("No", "No")], blank=True, null=True)
    fatigue = models.CharField(max_length=10, choices=[("Yes", "Yes"), ("No", "No")], blank=True, null=True)
    difficulty_breathing = models.CharField(max_length=10, choices=[("Yes", "Yes"), ("No", "No")], blank=True,
                                            null=True)
    ai_prediction = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.diagnosis_detail


class Prescription(models.Model):
    patient=models.ForeignKey('patient.Patient',on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor,on_delete=models.SET_NULL,null=True)
    prescription_date=models.DateField(auto_now_add=True)
    medication_detail=models.TextField(blank=True,null=True)
    dosage=models.TextField(blank=True,null=True)
    refill_count = models.IntegerField(default=0)
    prescription_till_date = models.DateField()

    medication_name=models.TextField(blank=True,null=True)



    def __str__(self):
        return self.prescription_date



class Department(models.Model):
    department_name=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.department_name} "




class Staff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="staff_profile",null=True, blank=True)


    name = models.CharField(max_length=100)
    role = models.CharField(
        max_length=50,
        choices=[

            ('Nurse', 'Nurse'),
            ('Technician', 'Technician'),
            ('Receptionist', 'Receptionist'),
            ('Administrator', 'Administrator'),
            ('Billing', 'Billing'),
        ]
    )
    contact_info = PhoneNumberField(unique=True, region="PK")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    shift_timings = models.CharField(max_length=50)
    date_hired = models.DateField(auto_now_add=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    #permission_level = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.role})"
