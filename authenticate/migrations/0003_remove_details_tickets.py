# Generated by Django 4.1.6 on 2023-02-28 02:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0002_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='details',
            name='tickets',
        ),
    ]