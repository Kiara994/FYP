from django.db import models
from django.utils.timezone import now
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class LabTest(models.Model):
    patient = models.ForeignKey('patient.Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctor.Doctor', on_delete=models.SET_NULL, null=True)
    technician = models.ForeignKey('doctor.Staff', on_delete=models.SET_NULL, null=True)
    test_name = models.CharField(max_length=50)
    test_description = models.TextField()
    test_date = models.DateTimeField()
    test_time = models.TimeField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ], default='pending')
    results = models.TextField(blank=True, null=True)
    report_generated_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.status == 'pending' and self.test_date and self.test_date < now():
            self.status = 'completed'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.test_name}"


class Lab(models.Model):
    lab_name = models.CharField(max_length=50)
    description = models.TextField()
    contact_number=PhoneNumberField(unique=True,region='PK')
    def __str__(self):
        return f"{self.lab_name}"
