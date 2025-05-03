from datetime import date

from django.core.exceptions import ValidationError
from django.db import models

##############  update status
from datetime import datetime, date, time

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('No-Show', 'No-Show'),
        ('Rescheduled', 'Rescheduled'),
    ]

    APPOINTMENT_TYPE_CHOICES = [
        ('In-Person', 'In-Person'),
        ('Virtual', 'Virtual'),
        ('Emergency', 'Emergency'),
        ('Follow-Up', 'Follow-Up'),
        ('Routine Checkup', 'Routine Checkup'),
    ]

    patient = models.ForeignKey('patient.Patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctor.Doctor', on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Scheduled')
    appointment_type = models.CharField(max_length=50, choices=APPOINTMENT_TYPE_CHOICES, default='In-Person')

    def clean(self):
        if self.appointment_date < date.today():
            raise ValidationError("You cannot select a past date for an appointment.")

    def current_status(self):
        now = datetime.now()
        appointment_datetime = datetime.combine(self.appointment_date, self.appointment_time)

        if self.status in ['Cancelled', 'No-Show', 'Rescheduled']:
            return self.status
        elif appointment_datetime < now:
            return 'Completed'
        elif appointment_datetime.date() == date.today():
            return 'Scheduled'
        else:
            return 'Scheduled'

    def __str__(self):
        return f"{self.appointment_date} - {self.doctor}"
