# Generated by Django 3.0.5 on 2020-07-16 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0014_auto_20200714_0401'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='correct_answers_count',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='total_questions',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
