from django.db import models
from categories.models import Category
from transactions.models import TransactionType


class TransactionTypeCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    transaction_type = models.ForeignKey(
        TransactionType, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        unique_together = ('category', 'transaction_type')

    def __str__(self):
        return f'{self.transaction_type.name} - {self.category.name}'
