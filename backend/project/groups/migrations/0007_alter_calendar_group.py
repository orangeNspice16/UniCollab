# Generated by Django 3.2 on 2021-04-20 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0006_calendar_eventname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='groups.group'),
        ),
    ]
