# Generated by Django 3.1.1 on 2020-09-30 14:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0004_auto_20200930_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 30, 14, 21, 37, 586966, tzinfo=utc)),
        ),
    ]
