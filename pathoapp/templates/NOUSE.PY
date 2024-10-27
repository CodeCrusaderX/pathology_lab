from django import forms
from .models import PatientMaster, UrineTest

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female')
]

class UrineTestForm(forms.ModelForm):
    patient_id = forms.ModelChoiceField(queryset=PatientMaster.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = UrineTest
        fields = [
            'testid', 'patientid', 'name', 'age', 'gender', 'mobile', 'email', 
            'colour', 'clarity', 'glucose', 'ketone', 'blood', 'ph', 
            'other_test', 'result', 'normal_value', 'testdate'
        ]
        widgets = {
            'testid': forms.TextInput(attrs={'class': 'form-control'}),
            'patientid': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
           
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'colour': forms.NumberInput(attrs={'class': 'form-control'}),
            'clarity': forms.NumberInput(attrs={'class': 'form-control'}),
            'glucose': forms.NumberInput(attrs={'class': 'form-control'}),
            'ketone': forms.NumberInput(attrs={'class': 'form-control'}),
            'blood': forms.NumberInput(attrs={'class': 'form-control'}),
            'ph': forms.NumberInput(attrs={'class': 'form-control'}),
            'other_test': forms.NumberInput(attrs={'class': 'form-control'}),
            'result': forms.NumberInput(attrs={'class': 'form-control'}),
            'normal_value': forms.NumberInput(attrs={'class': 'form-control'}),
             'testdate': forms.DateInput(attrs={'class': 'form-control', 'id':'datepicker'}),
        }