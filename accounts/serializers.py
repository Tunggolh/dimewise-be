from rest_framework import serializers

from .models import Account, AccountType


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = '__all__'


class AccountListSerializer(serializers.ModelSerializer):
    account_type = AccountTypeSerializer()

    class Meta:
        model = Account
        fields = ['id', 'name', 'account_type', 'balance']


class AccountDetailSerializer(serializers.ModelSerializer):
    account_type = AccountTypeSerializer()

    class Meta:
        model = Account
        fields = '__all__'
