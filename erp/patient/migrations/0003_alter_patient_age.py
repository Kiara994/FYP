# Generated by Django 5.0.12 on 2025-03-17 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_patient_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='age',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
