# Generated by Django 5.0.12 on 2025-04-04 05:15

import erp.users.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_user_is_registered'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', erp.users.managers.UserManager()),
            ],
        ),
    ]
