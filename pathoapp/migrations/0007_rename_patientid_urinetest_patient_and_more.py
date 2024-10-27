# Generated by Django 5.1.1 on 2024-10-03 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pathoapp', '0006_alter_urinetest_patientid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='urinetest',
            old_name='patientid',
            new_name='patient',
        ),
        migrations.RemoveField(
            model_name='urinetest',
            name='age',
        ),
        migrations.RemoveField(
            model_name='urinetest',
            name='email',
        ),
        migrations.RemoveField(
            model_name='urinetest',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='urinetest',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='urinetest',
            name='name',
        ),
        migrations.AlterField(
            model_name='urinetest',
            name='normal_value',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='urinetest',
            name='other_test',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='urinetest',
            name='ph',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='urinetest',
            name='result',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='urinetest',
            name='testdate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='urinetest',
            name='testid',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
    ]