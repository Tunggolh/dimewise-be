# Generated by Django 5.0.3 on 2024-05-11 14:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0002_add_parent_attribute_in_category_table'),
        ('transactions', '0001_add_transactions_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionTypeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.category')),
                ('transaction_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='transactions.transactiontypes')),
            ],
            options={
                'unique_together': {('category', 'transaction_type')},
            },
        ),
    ]
