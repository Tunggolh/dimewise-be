"""
Django admin configuration
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User
from categories.models import Category
from transactions.models import TransactionType, Transaction
from api.models import UserTransactionCategory
from accounts.models import Account, AccountType


class UserAdmin(BaseUserAdmin):
    """
    Custom user admin
    """
    ordering = ['id']
    list_display = ['email', 'first_name', 'last_name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
        }),
    )
    readonly_fields = ('last_login',)


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(TransactionType)
admin.site.register(Transaction)
admin.site.register(UserTransactionCategory)
admin.site.register(Account)
admin.site.register(AccountType)
