# Generated by Django 3.1.1 on 2020-09-30 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_user_full_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='email_login',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='user',
            name='full_name',
        ),
    ]
