# Generated by Django 5.0.1 on 2024-01-26 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diabetes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='diabetes_type',
            field=models.CharField(choices=[('Type 1', 'Type 1'), ('Type 2', 'Type 2')], default='Type 2', max_length=20),
        ),
    ]
