# Generated by Django 4.2.7 on 2023-12-04 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('-created_at',)},
        ),
    ]
