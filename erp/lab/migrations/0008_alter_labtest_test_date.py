# Generated by Django 5.1.6 on 2025-05-03 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0007_alter_labtest_test_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labtest',
            name='test_date',
            field=models.DateTimeField(),
        ),
    ]
