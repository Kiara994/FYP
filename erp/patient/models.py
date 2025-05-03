from datetime import date
# Create your models here.
from tkinter.constants import CASCADE

from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),

]
BLOOD_TYPES = [
    ("A+", "A+"),
    ("A-", "A-"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("O+", "O+"),
    ("O-", "O-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
]
class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patient_profile",null=True, blank=True)

    name=models.CharField(max_length=70,)
    date_of_birth=models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    contact_info=PhoneNumberField(unique=True,region='PK')
    emergency_contact_info=PhoneNumberField(region='PK')
    blood_type=models.CharField(max_length=3, choices=BLOOD_TYPES)
    medical_history=models.TextField(blank=True, null=True)
    address=models.TextField(blank=True, null=True)
    doctor_attending=models.ForeignKey('doctor.Doctor',on_delete=models.SET_NULL,null=True)
    insurance_detail = models.ForeignKey('billing.Insurance', on_delete=models.SET_NULL, null=True,related_name='patient_insurance')
    age=models.PositiveIntegerField(default=0,editable=False)

    def save(self, *args, **kwargs):
        """Calculate age before saving the patient instance."""
        if self.date_of_birth:
            today = date.today()
            self.age = today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ID: {self.id} - {self.name}"
