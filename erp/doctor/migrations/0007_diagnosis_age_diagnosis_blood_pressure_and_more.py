# Generated by Django 5.0.12 on 2025-03-28 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0006_diagnosis_ai_prediction'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnosis',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='blood_pressure',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='cholesterol_level',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='cough',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='difficulty_breathing',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='fatigue',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='fever',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, null=True),
        ),
    ]
