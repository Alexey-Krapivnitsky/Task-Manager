# Generated by Django 3.1.1 on 2020-09-30 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0009_auto_20200930_2010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='auth_token',
            field=models.CharField(default='123', max_length=128),
        ),
    ]