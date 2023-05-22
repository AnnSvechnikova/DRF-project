import datetime
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from datetime import date
from rest_framework import viewsets, status, filters
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from django.db.models import Max, Min
from rest_framework.views import APIView
from bookshop.serializers import *
from bookshop.models import Book, User, Order
import uuid
import logging
from bookshop.permissions import IsAdmin, IsManager
from rest_framework.generics import get_object_or_404
from importlib import import_module
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# Create your views here.
SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
storage = SessionStore()



class BookViewSet (viewsets.ModelViewSet):
    """api endpoint для просмотра и редактирования списка книг"""
    # queryset = Book.objects.all()
    serializer_class = BookSerializer
    # поиск на основе параметров запроса: http://example.com/api/users?search=value
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'get_price_range']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action in ['post', 'create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsManager]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        srch = self.request.GET.get("search", None)
        if(srch):
            queryset = self.get_queryset().filter(title__icontains=srch)
        else:
            queryset = self.get_queryset()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        queryset = Book.objects.all()
        book = get_object_or_404(queryset, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        book = request.data
        book_serialized = BookSerializer(book)
        book_serialized.save()
        return Response(book_serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, **kwargs):
    
        print("upd")
        try:
            print(pk)
            b = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({'message': 'Такая книга не существует'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(b, data=request.data)
        #проверяем, что данные содержат все требуемые поля нужных типов
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, **kwargs):
        try:
            print(pk)
            Book.objects.get(pk=pk).delete()
        except Exception:
            return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)

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
    #queryset = Order.objects.all().order_by('-order_date')
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ['list', 'partial_update', 'destroy', 'create','order_states']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action in ['retrieve', 'update']:
            permission_classes = [IsManager]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Order.objects.all().order_by('-order_id')
        user_id = self.request.query_params.get('user_id')
        state = self.request.query_params.get('state')
        date_type = self.request.query_params.get('date_type')
        min_d = self.request.query_params.get('minDate')
        max_d = self.request.query_params.get('maxDate')
        if user_id:
            usr = User.objects.get(pk=user_id)
            if not usr.is_staff:
                queryset = queryset.filter(user_id=user_id)
        if state:
            queryset = queryset.filter(state=state)
        if date_type:
            dat = self.request.query_params.get('dat')
            if date_type == 'order':
                queryset = queryset.filter(order_date=dat)
            if date_type == 'deliv':
                queryset = queryset.filter(deliv_date=dat)
            if date_type == 'pay':
                queryset = queryset.filter(pay_date=dat)
        if min_d:
            queryset = queryset.filter(order_date__gte=min_d) # gte: >=
        if max_d:
            queryset = queryset.filter(order_date__lte=max_d) # lte: <=
        return queryset

    @action(detail=False, methods=['get'])
    def order_states(self, request):
        states = []
        for c in Order.OrderState.choices:
            states.append({'value': c[0], 'label': c[1]})
        try:
            return Response(states)
        except:
            return Response([], status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        serializer = OrderSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        queryset = Order.objects.all()
        order = get_object_or_404(queryset, pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        ord = request.data
        ord_serialized = OrderSerializer(ord)
        ord_serialized.save()
        return Response(ord_serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, **kwargs):
        try:
            ord = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'message': 'Заказ не существует'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(ord, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, **kwargs):
        try:
            Order.objects.get(pk=pk).delete()
        except Exception:
            return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)

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


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": "registration successful"}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    #@method_decorator(csrf_exempt)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer проверил не только наличие нужных полей, но и наличие такого пользователя
        response = Response(serializer.data, status=status.HTTP_200_OK)
        user = User.objects.get(username=serializer.data.get('username'))
        login(request, user)
        response.set_cookie(key='sessionid', value=storage.session_key, samesite='None', secure=True)
        return response


class LogoutAPIView(APIView):
    permission_classes = [AllowAny]


    def post(self, request):
        session_id = request.COOKIES.get('sessionid')
        if session_id:
            logout(request)
            response = Response({"status": "logout"}, status=status.HTTP_200_OK)
            response.delete_cookie('sessionid')
            return response
        return Response({"status": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in []:
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action in ['retrieve', 'list']:
            permission_classes = [IsManager]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        queryset = User.objects.all()
        usr = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(usr)
        return Response(serializer.data, status=status.HTTP_200_OK)
