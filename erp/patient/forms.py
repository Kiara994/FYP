from django import forms
from .models import Patient



class PatientRegistrationForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})  # Adds a date picker
    )
    class Meta:
        model=Patient
        fields= '__all__'
        exclude = ['user_id','user','date','doctor_attending',""]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make doctor_attending and insurance_detail optional
        # self.fields["doctor_attending"].required = False
        self.fields["insurance_detail"].required = False
