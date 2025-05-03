from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now

from .forms import BillingForm, PaymentForm
from .models import Billing
from ..patient.models import Patient


# Create your views here.
def billing_creation(request):
    if not hasattr(request.user, 'staff_profile'):
        return redirect("account_login")  # Only staff can access

    form = BillingForm()

    if request.method == "POST":
        form = BillingForm(request.POST)
        if form.is_valid():
            #billing = form.save(commit=False)  # Don't save yet
            #doctor.user = request.user  # Associate with logged-in user
            form=BillingForm(request.POST)
            form.save()
            return redirect("doctor:dashboard")

    return render(request, "billing/create_bill.html", {"form": form})


def patient_billing(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    bills = Billing.objects.filter(patient=patient)
    return render(request, "billing/patient_billing_page.html", {"patient": patient, "bills": bills})



@login_required
def pay_bill(request, bill_id):
    bill = get_object_or_404(Billing, id=bill_id, patient=request.user.patient_profile)

    if request.method == "POST":
        form = PaymentForm(request.POST, bill=bill)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.bill = bill
            payment.save()

            # # Update bill status
            # bill.date_paid = now().date()
            # total_paid = sum(payment.amount_paid for payment in bill.payments.all())
            # if total_paid >= bill.amount:
            #     bill.status = "Paid"
            # bill.save()
            bill.date_paid = now().date()
            bill.status = "Paid"
            bill.save()

            return redirect("billing:patient_billing",patient_id=request.user.patient_profile.id)
    else:
        form = PaymentForm(bill=bill)

    return render(request, "billing/pay_bill.html", {"bill": bill, "form": form})
