# Generated by Django 3.2 on 2021-04-16 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='preferredmeetingEndTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='preferredmeetingStartTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]