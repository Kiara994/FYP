from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from erp.appointment.models import Appointment
from erp.doctor.models import Prescription
from erp.doctor.forms import DoctorRegistrationForm,StaffRegistrationForm,PrescriptionForm,DiagnosisForm
from erp.patient.views import home
from ..lab.models import LabTest
from ..patient.models import Patient
import joblib
import pandas as pd
import os
from django.shortcuts import render, redirect
from .forms import DiagnosisForm
from .models import Diagnosis
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DoctorRegistrationForm
from .models import Doctor
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import StaffRegistrationForm
from .models import Staff


@login_required
def doctor_dashboard(request):
    if not hasattr(request.user, 'doctor_profile') or request.user.doctor_profile is None:
        return redirect("account_login")  # Redirect if the user has no doctor profile

    doctor = request.user.doctor_profile  # ✅ Fix: Use `doctor_profile`
    appointments = Appointment.objects.filter(doctor=doctor).order_by("-appointment_date")[:5]
    prescriptions = Prescription.objects.filter(doctor=doctor).order_by("-prescription_date")[:5]

    context = {
        "doctor": doctor,
        "appointments": appointments,
        "prescriptions": prescriptions,
    }

    return render(request, "doctor/doctor_dashboard.html", context)






############## staff DASHBOARD LABTEST RESUSLT         #########

@login_required
def staff_dashboard(request):
    if not hasattr(request.user, 'staff_profile') or request.user.staff_profile is None:
        return redirect("account_login")

    staff = request.user.staff_profile

    lab_tests = []
    if staff.role == 'Technician':
        lab_tests = LabTest.objects.filter(
            technician=staff,
            status='completed'
        ).order_by('-test_date')

    context = {
        "staff": staff,
        "lab_tests": lab_tests,
    }

    return render(request, "doctor/staff_dashboard.html", context)














@login_required
def doctor_registration(request):
    user = request.user  # Get the logged-in user

    # Prevent duplicate registration
    if user.is_registered:
        return redirect("doctors:dashboard")  # Redirect if already registered

    form = DoctorRegistrationForm()

    if request.method == "POST":
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            doctor = form.save(commit=False)  # Don't save yet
            doctor.user = request.user  # Associate with logged-in user
            doctor.save()  # Now save to database

            request.user.is_registered = True  # Mark as registered
            request.user.save()

            return redirect("doctor:dashboard")  # Redirect to doctor dashboard

    return render(request, "doctor/doctor_registration.html", {"form": form})








@login_required
def staff_registration(request):
    user = request.user  # Get the logged-in user

    # Prevent duplicate registration
    if user.is_registered:
        return redirect("doctor:dashboard")  # Redirect if already registered

    form = StaffRegistrationForm()

    if request.method == "POST":
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            staff = form.save(commit=False)  # Don't save yet
            staff.user = request.user  # Associate with logged-in user
            staff.save()  # Now save to database

            request.user.is_registered = True  # Mark as registered
            request.user.save()

            return redirect("doctor:staff_dashboard")  # Redirect to staff dashboard

    return render(request, "doctor/staff_registration.html", {"form": form})



def prescribe_prescription(request,doctor_id):
    if not hasattr(request.user, 'doctor_profile'):
        return redirect("account_login")  # Only staff can access
    form=PrescriptionForm()
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription= form.save(commit=False)  # Don't save yet
            prescription.doctor = request.user.doctor_profile
            prescription.save()
            return redirect("doctor:dashboard")  # Redirect to staff dashboard



    return render(request, "doctor/prescribe_prescription.html", {"form":form})










#
# def doctor_diagnosis(request, doctor_id):
#     if not hasattr(request.user, 'doctor_profile'):
#         return redirect("account_login")  # Only doctors can access
#
#     form = DiagnosisForm()
#
#     if request.method == "POST":
#         form = DiagnosisForm(request.POST)
#         if form.is_valid():
#             diagnosis = form.save(commit=False)  # Don't save yet
#
#             # Associate doctor with the diagnosis
#             diagnosis.doctor = request.user.doctor_profile
#
#             # Generate AI-based prediction
#             symptoms_text = form.cleaned_data.get("symptoms")  # Get symptoms input
#             diagnosis.ai_prediction = predict_disease(symptoms_text)  # AI-generated diagnosis
#
#             diagnosis.save()  # Now save the instance with AI prediction
#             return redirect("doctor:dashboard")  # Redirect to doctor's dashboard
#
#     return render(request, "doctor/diagnosis.html", {"form": form})


























# Load the trained AI model (Choose RF or XGBoost)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "disease_prediction_model_rf11.pkl")  # Change to "disease_prediction_model_xgb.pkl" if needed
model, preprocessor, label_encoder,feature_columns = joblib.load(MODEL_PATH)


                       ########## text ai disease appear

def predict_disease(input_data):
    """
    Predicts disease based on user input.
    """
    try:
        print(f"Received input: {input_data}")  # Debugging

        # Load model and preprocessing objects
        # model, preprocessor, label_encoder, feature_columns = joblib.load("disease_prediction_model_rf.pkl")

        # Convert input into DataFrame
        input_df = pd.DataFrame([input_data])

        # Encode binary values (Yes/No → 1/0)
        binary_cols = ["Fever", "Cough", "Fatigue", "Difficulty Breathing"]
        for col in binary_cols:
            if col in input_df.columns:
                input_df[col] = input_df[col].map({"Yes": 1, "No": 0})

        # Ensure input has the same features as training data
        input_df = input_df.reindex(columns=feature_columns, fill_value=0)

        # Apply preprocessing (One-hot encoding + Scaling)
        input_transformed = preprocessor.transform(input_df)

        # Make prediction (returns an encoded number)
        prediction_encoded = model.predict(input_transformed)

        # Decode the prediction to get the actual disease name
        prediction = label_encoder.inverse_transform(prediction_encoded)[0]

        print(f"Predicted disease: {prediction}")  # Debugging
        return prediction
    except Exception as e:
        print(f"Prediction Error: {str(e)}")  # Debugging
        return f"Prediction Error: {str(e)}"




























################### ai disease name saved
def doctor_diagnosis(request, doctor_id):
    if not hasattr(request.user, 'doctor_profile'):
        return redirect("account_login")  # Restrict to doctors only

    form = DiagnosisForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        diagnosis = form.save(commit=False)  # Don't save yet

        diagnosis.doctor = request.user.doctor_profile  # Assign the doctor

        # Get user input
        input_data = {
            "Gender": form.cleaned_data["gender"],
            "Age": form.cleaned_data["age"],
            "Blood Pressure": form.cleaned_data["blood_pressure"],
            "Cholesterol Level": form.cleaned_data["cholesterol_level"],
            "Fever": form.cleaned_data["fever"],
            "Cough": form.cleaned_data["cough"],
            "Fatigue": form.cleaned_data["fatigue"],
            "Difficulty Breathing": form.cleaned_data["difficulty_breathing"],
        }

        # AI Diagnosis Prediction
        ai_disease = predict_disease(input_data)  # ✅ Fix: Prediction returns disease name

        diagnosis.ai_prediction = ai_disease  # ✅ Save actual disease name, not a number
        diagnosis.save()  # Now save to database

        return redirect("doctor:edit_diagnosis", diagnosis_id=diagnosis.id)  # Redirect to editing page

    return render(request, "doctor/diagnosis.html", {"form": form})

















def edit_diagnosis(request, diagnosis_id):
    diagnosis = get_object_or_404(Diagnosis, id=diagnosis_id)

    if request.method == "POST":
        form = DiagnosisForm(request.POST, instance=diagnosis)
        if form.is_valid():
            diagnosis = form.save(commit=False)

            # AI Prediction (if you want to re-run AI on updates)
            if not diagnosis.ai_prediction:  # Avoid overwriting existing predictions
                diagnosis.ai_prediction = predict_disease(diagnosis.diagnosis_detail)

            diagnosis.save()
            return redirect("doctor:dashboard")  # Redirect to detail page

    else:
        form = DiagnosisForm(instance=diagnosis)

    return render(request, "doctor/edit_diagnosis.html", {"form": form, "diagnosis": diagnosis})





###########################      auto age gendefr       ##########################
def get_patient_info(request):
    patient_id = request.GET.get("patient_id")
    try:
        patient = Patient.objects.get(id=patient_id)
        data = {
            "gender": patient.gender,
            "age": patient.age
        }
    except Patient.DoesNotExist:
        data = {"error": "Patient not found"}

    return JsonResponse(data)

