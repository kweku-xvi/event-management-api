# Generated by Django 4.2.7 on 2023-12-05 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_app', '0005_alter_registration_date_registered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='date_registered',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
