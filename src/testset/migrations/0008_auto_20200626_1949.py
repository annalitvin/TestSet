# Generated by Django 3.0.5 on 2020-06-26 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('testset', '0007_auto_20200624_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresultdetail',
            name='variant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='test_result_details', to='testset.Variant'),
        ),
    ]
