from django import forms
from .models import LabTest
from erp.patient.models import Patient
from erp.doctor.models import Doctor
from django_select2.forms import ModelSelect2Widget


class DoctorSelect2Widget(ModelSelect2Widget):
    model = Doctor
    search_fields = [
        'id__icontains',     # Patient ID
        'name__icontains',   # Patient Name
    ]

    def label_from_instance(self, obj):
        return f"{obj.id} - {obj.name}"

class PatientSelect2Widget(ModelSelect2Widget):
    model = Patient
    search_fields = [
        'id__icontains',     # Patient ID
        'name__icontains',   # Patient Name
    ]

    def label_from_instance(self, obj):
        return f"{obj.id} - {obj.name}"

class CreateLabTestForm(forms.ModelForm):
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
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        widget=DoctorSelect2Widget(
            # attrs={'data-minimum-input-lengt-placeholder': 'Search by Patient ID or Name', 'class': 'form-control'}
            attrs={

                'data-placeholder': 'Search by Doctor ID or Name',
                'data-minimum-input-length': 1,
                'class': 'form-control'
            }
        )
    )


    test_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})  # Adds a date picker
    )
    test_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})  # Adds a time picker
    )

    class Meta:
        model = LabTest
        fields = "__all__"
        exclude = ['results',"report_generated_date","status","technician"]







############################                         LABTEST RESULT UPDATION           ################


class LabTestResultForm(forms.ModelForm):
    class Meta:
        model = LabTest
        fields = ['results']  # Let the technician only edit results

    def save(self, commit=True):
        lab_test = super().save(commit=False)
        from django.utils.timezone import now
        lab_test.report_generated_date = now()  # Set report generated time
        if commit:
            lab_test.save()
        return lab_test
