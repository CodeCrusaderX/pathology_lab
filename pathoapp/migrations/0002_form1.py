# Generated by Django 5.1.1 on 2024-09-29 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pathoapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Form1',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
                ('stuname', models.CharField(max_length=100)),
                ('fathername', models.CharField(max_length=255)),
            ],
        ),
    ]