# Generated by Django 2.2.6 on 2020-01-04 03:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swiper', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='swiper',
            old_name='stime',
            new_name='s_time',
        ),
    ]
