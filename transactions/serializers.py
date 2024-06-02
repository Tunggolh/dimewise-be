from rest_framework import serializers
from .models import TransactionType, Transaction, Category, Account


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'name', 'account_type', 'balance']
        read_only_fields = ['id']


class AccountDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'
        read_only_fields = ['id']


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']


class TransactionListSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    account = serializers.ReadOnlyField(source='account.name')
    transaction_type = TransactionTypeSerializer()

    class Meta:
        model = Transaction
        fields = ['id', 'transaction_type',
                  'amount', 'date', 'category', 'account']


class TransactionDetailSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    account = serializers.ReadOnlyField(source='account.name')
    transaction_type = TransactionTypeSerializer()

    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
