from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Account(models.Model):
    account_type = models.CharField(max_length=3)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class TransactionType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    transaction_type = models.ForeignKey(
        TransactionType, models.CASCADE, related_name='transaction_type')
    user = models.ForeignKey(
        get_user_model(), models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name


class Transaction(models.Model):
    transaction_type = models.ForeignKey(
        TransactionType, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='transactions')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE)
    account = models.ForeignKey('contenttypes.ContentType',
                                on_delete=models.CASCADE,
                                related_name='transactions')

    def __str__(self):
        return f'{self.transaction_type.name} - {self.amount} on {self.date}'
