# Generated by Django 3.0.5 on 2020-06-27 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0007_auto_20200627_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avr_score',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
