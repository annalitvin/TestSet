# Generated by Django 3.0.5 on 2020-06-16 06:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0004_auto_20200616_0648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
    ]
