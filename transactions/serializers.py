from rest_framework import serializers
from .models import TransactionType, Transaction


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = '__all__'


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
