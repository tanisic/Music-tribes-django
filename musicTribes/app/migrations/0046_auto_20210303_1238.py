# Generated by Django 3.1.5 on 2021-03-03 11:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0045_auto_20210303_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='song_duration',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 3, 11, 38, 52, 824475, tzinfo=utc)),
        ),
    ]
