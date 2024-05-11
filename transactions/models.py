from django.db import models
from django.conf import settings


class TransactionType(models.Model):
    name = models.CharField(max_length=255)

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
    category = models.ForeignKey('contenttypes.ContentType',
                                 on_delete=models.CASCADE)
    account = models.ForeignKey('contenttypes.ContentType',
                                on_delete=models.CASCADE,
                                related_name='transactions')

    def __str__(self):
        return f'{self.transaction_type.name} - {self.amount} on {self.date}'
