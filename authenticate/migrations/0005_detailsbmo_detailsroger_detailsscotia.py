# Generated by Django 4.1.6 on 2023-02-28 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticate', '0004_details_totaltickets'),
    ]

    operations = [
        migrations.CreateModel(
            name='Detailsbmo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats', models.CharField(default='', max_length=80)),
                ('namefirst', models.CharField(default='', max_length=80)),
                ('namelast', models.CharField(default='', max_length=80)),
                ('emailcust', models.EmailField(default='', max_length=80)),
                ('phone', models.CharField(default='', max_length=80)),
                ('totaltickets', models.CharField(default='', max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Detailsroger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats', models.CharField(default='', max_length=80)),
                ('namefirst', models.CharField(default='', max_length=80)),
                ('namelast', models.CharField(default='', max_length=80)),
                ('emailcust', models.EmailField(default='', max_length=80)),
                ('phone', models.CharField(default='', max_length=80)),
                ('totaltickets', models.CharField(default='', max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Detailsscotia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats', models.CharField(default='', max_length=80)),
                ('namefirst', models.CharField(default='', max_length=80)),
                ('namelast', models.CharField(default='', max_length=80)),
                ('emailcust', models.EmailField(default='', max_length=80)),
                ('phone', models.CharField(default='', max_length=80)),
                ('totaltickets', models.CharField(default='', max_length=80)),
            ],
        ),
    ]