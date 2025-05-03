from django import forms
from .models import Doctor,Staff,Prescription,Diagnosis
from erp.patient.models import Patient
from django_select2.forms import ModelSelect2Widget






class DoctorRegistrationForm(forms.ModelForm):
    class Meta:
        model=Doctor
        fields="__all__"
        exclude=['availability','shift_timings',"user_id",'salary','user']



class StaffRegistrationForm(forms.ModelForm):
    class Meta:
        model=Staff
        fields="__all__"
        exclude=['shift_timings','salary','user']

class PatientSelect2Widget(ModelSelect2Widget):
    model = Patient
    search_fields = [
        'id__icontains',     # Patient ID
        'name__icontains',   # Patient Name
    ]

    def label_from_instance(self, obj):
        return f"{obj.id} - {obj.name}"

class PrescriptionForm(forms.ModelForm):
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        widget=PatientSelect2Widget(
            # attrs={'data-minimum-input-lengt-placeholder': 'Search by Patient ID or Name', 'class': 'form-control'}
            attrs={

                'data-placeholder': 'Search by Patient ID or Name',
                'data-minimum-input-length': 1,
                'class': 'form-control',
                'style': 'width: 100%',
            }
        )
    )
    prescription_till_date=forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})  # Adds a date picker
    )
    class Meta:
        model=Prescription
        fields="__all__"
        exclude=["doctor"]

#

class DiagnosisForm(forms.ModelForm):
    # diagnosis_date=forms.DateField(
    #     widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})  # Adds a date picker
    # )
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        widget=PatientSelect2Widget(
            # attrs={'data-minimum-input-lengt-placeholder': 'Search by Patient ID or Name', 'class': 'form-control'}
            attrs={

                'data-placeholder': 'Search by Patient ID or Name',
                'data-minimum-input-length': 1,
                'class': 'form-control'
            }
        )
    )
    class Meta:
        model=Diagnosis
        # fields="__all__"
        # exclude=["doctor",'diagnosis_date']
        fields = ["patient", "symptoms", "gender", "age", "blood_pressure", "cholesterol_level", "fever", "cough",
                  "fatigue", "difficulty_breathing","tests_ordered","diagnosis_detail"]
        exclude = ["doctor", "diagnosis_date", "ai_prediction"]  # AI prediction should be generated automatically
        widgets = {
            "diagnosis_detail": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "tests_ordered": forms.Textarea(attrs={"class": "form-control", "rows": 3}),

        }

#     ai_prediction = forms.CharField(required=False, disabled=True)
#




# class DiagnosisForm(forms.ModelForm):
#     class Meta:
#         model = Diagnosis
#         fields = ["patient", "symptoms", "gender", "age", "blood_pressure", "cholesterol_level",
#                   "fever", "cough", "fatigue", "difficulty_breathing", "tests_ordered", "diagnosis_detail"]
#         exclude = ["doctor", "diagnosis_date", "ai_prediction"]
#         widgets = {
#             "gender": forms.TextInput(attrs={"readonly": "readonly", "class": "form-control", "id": "id_gender"}),
#             "age": forms.NumberInput(attrs={"readonly": "readonly", "class": "form-control", "id": "id_age"}),
#         }











# #autofill
# class DiagnosisForm(forms.ModelForm):
#     class Meta:
#         model = Diagnosis
#         fields = ["patient", "symptoms", "gender", "age", "blood_pressure", "cholesterol_level", "fever", "cough",
#                   "fatigue", "difficulty_breathing", "tests_ordered", "diagnosis_detail"]
#         exclude = [ "ai_prediction"]  # AI prediction will be auto-generated
#         widgets = {
#             "patient": forms.Select(attrs={"class": "form-select", "id": "id_patient"}),
#             "gender": forms.TextInput(attrs={"readonly": "readonly", "class": "form-control", "id": "id_gender"}),
#             "age": forms.NumberInput(attrs={"readonly": "readonly", "class": "form-control", "id": "id_age"}),
#             "diagnosis_detail": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
#             "tests_ordered": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
#         }
#     ai_prediction = forms.CharField(required=False, disabled=True)
