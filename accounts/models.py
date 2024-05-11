from django.db import models
from django.conf import settings


class AccountTypes(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Account(models.Model):
    account_type = models.ForeignKey(AccountTypes, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.name
