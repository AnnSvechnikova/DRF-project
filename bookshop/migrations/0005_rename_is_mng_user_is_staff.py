# Generated by Django 4.1.3 on 2023-02-21 03:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookshop', '0004_alter_user_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_mng',
            new_name='is_staff',
        ),
    ]