from rest_framework import serializers

from .models import Account, AccountType


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = '__all__'
        read_only_fields = ['id']


class AccountSerializer(serializers.ModelSerializer):
    account_type = AccountTypeSerializer()

    class Meta:
        model = Account
        fields = ['id', 'name', 'account_type', 'balance']
        read_only_fields = ['id']


class AccountDetailSerializer(serializers.ModelSerializer):
    account_type = AccountTypeSerializer()

    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ['id']
