# Generated by Django 4.1.6 on 2023-02-28 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0003_remove_details_tickets'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='totaltickets',
            field=models.CharField(default='', max_length=80),
        ),
    ]
