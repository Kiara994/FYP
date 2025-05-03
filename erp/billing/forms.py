from decimal import Decimal

from django import forms
from .models import Billing, Payment
from erp.patient.models import Patient

from django_select2.forms import ModelSelect2Widget

class PatientSelect2Widget(ModelSelect2Widget):
    model = Patient
    search_fields = [
        'id__icontains',     # Patient ID
        'name__icontains',   # Patient Name
    ]

    def label_from_instance(self, obj):
        return f"{obj.id} - {obj.name}"
class BillingForm(forms.ModelForm):

    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        widget=PatientSelect2Widget(
            # attrs={'data-minimum-input-lengt-placeholder': 'Search by Patient ID or Name', 'class': 'form-control'}
            attrs={

                'data-placeholder': 'Search by Patient ID or Name',
                'data-minimum-input-length': 1,
                'class': 'form-control',
                'style': 'width: 100%',}

        )
    )
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})  # Adds a date picker
    )

    class Meta:
        model = Billing
        exclude=["status","billing_date","date_paid","payment_method","insurance_coverage"]


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount_paid', 'payment_method']

    def __init__(self, *args, **kwargs):
        bill = kwargs.pop('bill', None)  # Get the bill object
        super().__init__(*args, **kwargs)

        if bill:
            self.bill = bill  # ✅ Assign bill to self.bill
            remaining_amount = bill.amount  # Default to full amount

            # If patient has insurance, deduct co-pay
            if bill.patient.insurance_detail:
                remaining_amount -= bill.patient.insurance_detail.co_pay or Decimal(0)

            # Ensure patient can only pay the exact remaining amount
            self.fields['amount_paid'].widget.attrs['max'] = remaining_amount
            self.fields['amount_paid'].initial = remaining_amount  # Auto-fill remaining amount

    def clean_amount_paid(self):
        """Ensure the amount paid is exactly the remaining balance after insurance."""
        amount_paid = self.cleaned_data.get("amount_paid")

        # ✅ Check if `self.bill` exists before using it
        if hasattr(self, "bill"):
            remaining_amount = self.bill.amount

            if self.bill.patient.insurance_detail:
                remaining_amount -= self.bill.patient.insurance_detail.co_pay or Decimal(0)

            if amount_paid != remaining_amount:
                raise forms.ValidationError(f"You must pay the exact remaining amount: ${remaining_amount}")

        return amount_paid
