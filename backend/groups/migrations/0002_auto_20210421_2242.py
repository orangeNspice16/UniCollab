# Generated by Django 3.2 on 2021-04-21 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='skills',
            field=models.CharField(default='C', max_length=1000),
        ),
        migrations.AddField(
            model_name='groupmember',
            name='skills',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
