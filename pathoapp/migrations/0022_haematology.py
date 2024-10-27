# Generated by Django 5.1.1 on 2024-10-15 09:42

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pathoapp', '0021_delete_haematology'),
    ]

    operations = [
        migrations.CreateModel(
            name='Haematology',
            fields=[
                ('test_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('test_date', models.DateField(default=datetime.datetime.now)),
                ('haemoglobin', models.DecimalField(decimal_places=2, max_digits=5)),
                ('rbc_count', models.DecimalField(decimal_places=2, max_digits=5)),
                ('platelets', models.DecimalField(decimal_places=2, max_digits=5)),
                ('pcv', models.DecimalField(decimal_places=2, max_digits=5)),
                ('mcv', models.DecimalField(decimal_places=2, max_digits=5)),
                ('mch', models.DecimalField(decimal_places=2, max_digits=5)),
                ('mchc', models.DecimalField(decimal_places=2, max_digits=5)),
                ('reticulocyte_count', models.DecimalField(decimal_places=2, max_digits=5)),
                ('bleeding_time', models.DecimalField(decimal_places=2, max_digits=5)),
                ('clotting_time', models.DecimalField(decimal_places=2, max_digits=5)),
                ('eosinophil_exam', models.DecimalField(decimal_places=2, max_digits=5)),
                ('sickling_exam', models.CharField(max_length=100)),
                ('other_test', models.CharField(max_length=100)),
                ('result', models.CharField(max_length=100)),
                ('normal_value', models.CharField(max_length=100)),
                ('remarks', models.CharField(max_length=100)),
                ('patientname', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=10)),
                ('mobile', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pathoapp.patientmaster')),
            ],
        ),
    ]