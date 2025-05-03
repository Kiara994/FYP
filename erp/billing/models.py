from datetime import timedelta, date
from decimal import Decimal

from django.db import models
from django.db.models import DateTimeField
from django.utils.timezone import now
from psycopg2 import DATETIME


from django.db import models
from datetime import timedelta

class Billing(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Insurance', 'Insurance'),
    ]
    BILL_TYPE_CHOICES = [
        ('Doctor Appointment', 'Doctor Appointment'),
        ('Lab Test', 'Lab Test'),

    ]
    patient = models.ForeignKey('patient.Patient', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateTimeField(null=True, blank=True)  # Allowing it to be set dynamically
    status = models.CharField(max_length=10, choices=[
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Overdue', 'Overdue'),
    ], default='Pending')
    billing_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='Cash')
    insurance_coverage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_paid = models.DateTimeField(null=True, blank=True)
    bill_type = models.CharField(max_length=20, choices=BILL_TYPE_CHOICES, default="Other")
    #
    # def apply_insurance(self):
    #     """Applies insurance coverage if available."""
    #     if hasattr(self.patient, "insurance_detail"):
    #         insurance = self.patient.insurance_detail
    #         today = date.today()
    #
    #         # Ensure the policy is active
    #         if insurance.policy_start_date <= today <= insurance.policy_end_date:
    #             # Apply deductible (insurance coverage)
    #             self.insurance_coverage = min(self.amount, insurance.deductible or Decimal(0))
    #             self.amount_due = self.amount - self.insurance_coverage
    #             self.amount_due = max(self.amount_due, Decimal(0))  # Prevent negative amounts
    def apply_insurance(self):
        """Applies insurance coverage if available."""
        if self.patient.insurance_detail is not None:  # Check if insurance_detail exists
            insurance = self.patient.insurance_detail
            today = date.today()

            # Ensure the policy is active
            if insurance.policy_start_date <= today <= insurance.policy_end_date:
                # Apply deductible (insurance coverage)
                self.insurance_coverage = min(self.amount, insurance.deductible or Decimal(0))
                self.amount_due = self.amount - self.insurance_coverage
                self.amount_due = max(self.amount_due, Decimal(0))  # Prevent negative amounts
        else:
            self.insurance_coverage = Decimal(0)  # No insurance, no coverage
            self.amount_due = self.amount  # No discount from insurance

    def save(self, *args, **kwargs):
        """Automatically apply insurance coverage if available."""
        if not self.due_date:
            self.due_date = self.billing_date + timedelta(days=30)

        # Check if the patient has insurance
        if self.insurance_coverage is None:  # Apply insurance only if not already set
            self.apply_insurance()


        if self.date_paid:
            self.status = 'Paid'
        elif self.due_date and self.due_date < now() and self.status != 'Paid':
            self.status = 'Overdue'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Billing: {self.patient.name} - ${self.amount} (Due: {self.due_date})"


class Insurance(models.Model):
    patient = models.ForeignKey('patient.Patient', on_delete=models.CASCADE)
    provider_name = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=50, unique=True)
    coverage_details = models.TextField()
    co_pay = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    deductible = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    policy_start_date = models.DateField()
    policy_end_date = models.DateField()

    def __str__(self):
        return f"{self.policy_number} ({self.provider_name})"




class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Insurance', 'Insurance'),
    ]

    bill = models.ForeignKey(Billing, on_delete=models.CASCADE, related_name="payments")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Update billing status after payment."""
        super().save(*args, **kwargs)  # Save payment first

        # Update billing status
        total_paid = sum(payment.amount_paid for payment in self.bill.payments.all())
        if total_paid >= self.bill.amount:
            self.bill.status = "Paid"
            self.bill.date_paid = now().date()
        self.bill.save()

    def __str__(self):
        return f"Payment of ${self.amount_paid} for Bill {self.bill.id} on {self.payment_date}"
