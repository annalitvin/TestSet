# Generated by Django 3.0.5 on 2020-07-14 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0009_remove_user_number_tests_passed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='number_tests_passed',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
