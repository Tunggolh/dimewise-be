from django.db import models
from django.contrib.auth import get_user_model
from categories.models import Category
from transactions.models import TransactionType


class UserTransactionCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    transaction_type = models.ForeignKey(
        TransactionType, on_delete=models.CASCADE, related_name='categories')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        unique_together = ('category', 'transaction_type', 'user')

    def __str__(self):
        return f'{self.transaction_type.name} - {self.category.name}'
