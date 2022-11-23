from bookshop.models import Book
from bookshop.models import User
from bookshop.models import Order
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        #сериализуемая модель
        model = Book
        #сериализуемые поля
        fields = ["book_id", "title", "in_stock", "descr", "price", "picture"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "full_name", "login", "passwd"]


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["order_id", "user_id", "book_id", "amount", "order_date", "pay_date", "deliv_date", "state"]

