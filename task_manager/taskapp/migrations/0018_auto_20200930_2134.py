# Generated by Django 3.1.1 on 2020-09-30 16:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0017_auto_20200930_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 30, 16, 34, 7, 771151, tzinfo=utc)),
        ),
    ]