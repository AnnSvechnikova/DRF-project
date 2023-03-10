from bookshop.models import Book, User, Order
from rest_framework import serializers
from django.contrib.auth import authenticate


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        #сериализуемая модель
        model = Book
        #сериализуемые поля
        fields = ['book_id', 'title', 'in_stock', 'descr', 'price', 'picture']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 'user_id', 'book_id', 'amount', 'order_date', 'pay_date', 'deliv_date', 'state']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'username', 'password', 'full_name', 'is_staff', 'is_superuser']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=128, min_length=4, write_only=True)
    user_id = serializers.IntegerField(read_only=True)
    full_name = serializers.CharField(max_length=30, read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    def validate(self, data) -> User:
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError(
                'A username address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found.'
            )
        return user


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=30,
        min_length=4,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ('user_id', 'username', 'password', 'full_name', 'is_staff', 'is_superuser')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)




