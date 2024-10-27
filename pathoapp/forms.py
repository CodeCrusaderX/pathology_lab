from django import forms
from .models import *

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['doctorname', 'email']
        widgets = {
            'doctorname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }   


class PatientForm(forms.ModelForm):
    class Meta:
        model = PatientMaster
        fields = ['patientid', 'patientname', 'recondate', 'age', 'gender', 'mobile', 'email', 'address', 'refbydoctor']
        widgets = {
            'patientid': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Patient ID'}),
            'patientname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Patient Name'}),  # Updated field name
            'recondate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Age'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mobile Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter Address'}),
            'refbydoctor': forms.Select(attrs={'class': 'form-control'}),
        }


class HaematologyForm(forms.ModelForm):
    patient_id = forms.IntegerField(label="Patient ID", required=True)

    class Meta:
        model = Haematology
        fields = [
            'patient_id', 'test_date', 'haemoglobin', 'rbc_count', 'platelets',
            'pcv', 'mcv', 'mch', 'mchc', 'reticulocyte_count', 'bleeding_time', 'clotting_time',
            'eosinophil_exam', 'sickling_exam', 'other_test', 'result', 'normal_value', 'remarks'
        ]
        widgets = {
            'test_date': forms.DateInput(attrs={'type': 'date'}),
        }