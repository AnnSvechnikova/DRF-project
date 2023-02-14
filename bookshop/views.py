import datetime
from django.db.models import Min, Max
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from bookshop.serializers import BookSerializer, UserSerializer, OrderSerializer
from bookshop.models import Book, User, Order
from datetime import date


class BookViewSet (viewsets.ModelViewSet):
    """api endpoint для просмотра и редактирования списка книг"""
    # queryset = Book.objects.all()
    serializer_class = BookSerializer
    # поиск на основе параметров запроса: http://example.com/api/users?search=value
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    # метод для получения диапазона цен
    @action(detail=False, methods=['get'])
    def get_price_range(self, request):
        return Response(Book.objects.aggregate(min_pr=Min('price'), max_pr=Max('price')))

    def get_queryset(self):
        queryset = Book.objects.all()
        min_pr = self.request.query_params.get('minPrice')
        max_pr = self.request.query_params.get('maxPrice')
        if min_pr:
            queryset = queryset.filter(price__gte=min_pr) # gte: >=
        if max_pr:
            queryset = queryset.filter(price__lte=max_pr) # lte: <=
        return queryset


class UserViewSet (viewsets.ModelViewSet):
    """api endpoint для просмотра и редактирования списка пользователей"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class OrderViewSet (viewsets.ModelViewSet):
    """api endpoint для просмотра и редактирования списка заказов"""
    queryset = Order.objects.all().order_by('-order_date')
    serializer_class = OrderSerializer

    """метод для отбора заказов за нужную дату"""
    @action(detail=False)
    def get_by_date(self, request):
        if 'date' in request.data:
            d = datetime.datetime.strptime(request.data['date'], "%Y-%m-%d").date()
        else:
            d = date.today()
        result = len(list(filter(lambda x: x.order_date == d, Order.objects.all())))
        return Response({'date': d,
                        'amount': result})

    """"метод для получения книги из заказа"""
    @action(detail=False)
    def get_book_info(self, request):
        bookId = int(self.request.query_params.get('id'))
        result = [x for x in Book.objects.all() if x.book_id == bookId][0]
        return Response({'title': result.title,
                         'price': result.price
                         })







