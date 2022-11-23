import datetime

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from bookshop.serializers import BookSerializer, UserSerializer, OrderSerializer
from bookshop.models import Book, User, Order
from datetime import date


class BookViewSet (viewsets.ModelViewSet):
    """api endpoint для просмотра и редактирования списка книг"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class UserViewSet (viewsets.ModelViewSet):
    """api endpoint для просмотра и редактирования списка пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class OrderViewSet (viewsets.ModelViewSet):
    """api endpoint для просмотра и редактирования списка заказов"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    """добавим метод для отбора заказов за нужную дату"""
    @action(detail=False)
    def get_by_date(self, request):
        if 'date' in request.data:
            d = datetime.datetime.strptime(request.data['date'], "%Y-%m-%d").date()
        else:
            d = date.today()
        result = len(list(filter(lambda x: x.check_date(d), Order.objects.all())))
        return Response({'date': d,
                        'the amount of orders': result})





