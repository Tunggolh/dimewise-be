# Generated by Django 5.0.3 on 2024-05-11 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_add_transactions_table'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TransactionTypes',
            new_name='TransactionType',
        ),
    ]
