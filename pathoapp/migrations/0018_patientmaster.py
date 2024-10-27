# Generated by Django 5.1.1 on 2024-10-08 15:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pathoapp', '0017_remove_bloodsugartest_patient_delete_form1_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientMaster',
            fields=[
                ('patientid', models.IntegerField(primary_key=True, serialize=False)),
                ('patientname', models.CharField(max_length=100)),
                ('recondate', models.DateField()),
                ('age', models.IntegerField()),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')], default='MALE', max_length=10)),
                ('mobile', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=255)),
                ('refbydoctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pathoapp.doctor')),
            ],
        ),
    ]
