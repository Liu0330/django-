# Generated by Django 2.2.6 on 2020-01-04 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swiper', '0002_auto_20200104_1158'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid1', models.IntegerField()),
                ('uid2', models.IntegerField()),
            ],
        ),
    ]
