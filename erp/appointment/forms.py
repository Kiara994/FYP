from django import forms
from .models import Appointment
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


class PatientAppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.all(),
        widget=DoctorSelect2Widget(
            # attrs={'data-minimum-input-lengt-placeholder': 'Search by Patient ID or Name', 'class': 'form-control'}
            attrs={

                'data-placeholder': 'Search by Doctor ID or Name',
                'data-minimum-input-length': 1,
                'class': 'form-control',
                'style': 'width: 100%',
            }
        )
    )
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})  # Adds a date picker
    )
    appointment_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})  # Adds a time picker
    )
    class Meta:
        model=Appointment
        fields="__all__"
        exclude=['patient','status']





# class DoctorAppointmentForm(forms.ModelForm):
#     appointment_date = forms.DateField(
#         widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})  # Adds a date picker
#     )
#     appointment_time = forms.TimeField(
#         widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})  # Adds a time picker
#     )
#     class Meta:
#         model=Appointment
#         fields="__all__"
#         exclude=['doctor','status']

########## searchable part
class PatientSelect2Widget(ModelSelect2Widget):
    model = Patient
    search_fields = [
        'id__icontains',     # Patient ID
        'name__icontains',   # Patient Name
    ]

    def label_from_instance(self, obj):
        return f"{obj.id} - {obj.name}"
# class PatientSelect2Widget(ModelSelect2Widget):
#     model = Patient
#     search_fields = [
#         'id__icontains',
#         'name__icontains',
#     ]
#     # Optional: label display
#     def label_from_instance(self, obj):
#         return f"{obj.id} - {obj.name}"
#
#     def build_attrs(self, base_attrs, extra_attrs=None):
#         attrs = super().build_attrs(base_attrs, extra_attrs)
#         attrs['data-placeholder'] = 'Search Patient ID or Name'
#         attrs['data-minimum-input-length'] = 1
#         return attrs

class DoctorAppointmentForm(forms.ModelForm):
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

    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    appointment_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )

    class Meta:
        model = Appointment
        fields = "__all__"
        exclude = ['doctor', 'status']
        # widgets = {
        #     "patient": PatientSelect2Widget
        # }


class RescheduleAppointmentForm(forms.ModelForm):
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})  # Adds a date picker
    )
    appointment_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})  # Adds a time picker
    )
    class Meta:
        model=Appointment
        fields=['appointment_type','appointment_date']



