# Generated by Django 3.2 on 2021-04-21 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0003_alter_group_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='skills',
            field=models.CharField(default='C, Data Modelling, User Interfaces, SQLite, Algorithms', max_length=1000),
        ),
    ]
