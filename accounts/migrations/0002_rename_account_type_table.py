# Generated by Django 5.0.3 on 2024-05-11 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_add_accounts_table'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AccountTypes',
            new_name='AccountType',
        ),
    ]