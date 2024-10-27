from django.db import models
from datetime import datetime

# Create your models here.

class Doctor(models.Model):
    doctorname = models.CharField(max_length=255, primary_key=True)  # Field for doctor's name
    email = models.EmailField(max_length=254)  # Field for doctor's email address

    def __str__(self):
        return self.doctorname

class PatientMaster(models.Model):
    patientid = models.IntegerField(primary_key=True)  
    patientname = models.CharField(max_length=100)  # Renamed 'name' to 'patientname'
    recondate = models.DateField()  # Recommended date for the patient
    age = models.IntegerField()
    
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='MALE')
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=255)

    # Reference to Doctor model
    refbydoctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.patientname} ({self.patientid})"  # Now displaying patientname




class Haematology(models.Model):
    # Linking to PatientMaster model
    patient = models.ForeignKey(PatientMaster, on_delete=models.CASCADE)
   
    
    # Test details
    test_id = models.CharField(max_length=50, primary_key=True)  # Primary key for the test
    test_date = models.DateField(default=datetime.now)  # Automatically sets the current date

    # Haematology test fields
    haemoglobin = models.DecimalField(max_digits=5, decimal_places=2)
    rbc_count = models.DecimalField(max_digits=5, decimal_places=2)
    platelets = models.DecimalField(max_digits=5, decimal_places=2)
    pcv = models.DecimalField(max_digits=5, decimal_places=2)
    mcv = models.DecimalField(max_digits=5, decimal_places=2)
    mch = models.DecimalField(max_digits=5, decimal_places=2)
    mchc = models.DecimalField(max_digits=5, decimal_places=2)
    reticulocyte_count = models.DecimalField(max_digits=5, decimal_places=2)
    bleeding_time = models.DecimalField(max_digits=5, decimal_places=2)
    clotting_time = models.DecimalField(max_digits=5, decimal_places=2)
    eosinophil_exam = models.DecimalField(max_digits=5, decimal_places=2)
    sickling_exam = models.CharField(max_length=100)
    other_test = models.CharField(max_length=100)
    result = models.CharField(max_length=100)
    normal_value = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100)

    # Additional patient fields
    patientname = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return f"Haematology Test {self.test_id} for {self.patient.patientname}"

         

