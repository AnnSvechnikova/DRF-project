# Generated by Django 4.1.3 on 2023-02-21 03:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0002_remove_user_login_remove_user_passwd_user_groups_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_adm',
        ),
    ]
