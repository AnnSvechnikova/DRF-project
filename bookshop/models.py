# Create your models here.
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from bookshop.managers import UserManager


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    in_stock = models.IntegerField(default=0)
    descr = models.CharField(max_length=255)
    price = models.FloatField()
    picture = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'books'

    def __str__(self):
        return self.title or ' '


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=128, null=True)
    username = models.CharField(max_length=30, unique=True, null=True)
    full_name = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    # is admin === is_superuser, is manager === is_staff

    USERNAME_FIELD = 'username'

    objects = UserManager()

    class Meta:
        managed = True
        db_table = 'users'

    def __str__(self):
        return self.username or self.full_name


class Order(models.Model):
    class OrderState(models.TextChoices):
        #выбор значения поля из ограниченного числа вариантов:
        CREATED = 'CREATED', ('Создан')
        DELIVERED = 'DELIVERED', ('Доставлен')
        PAID = 'PAID', ('Оплачен')
        CANCELLED = 'CANCELLED', ('Отменен')

    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_column='order_id_id')
    book_id = models.ForeignKey(Book, models.DO_NOTHING, db_column='book_id_id')
    amount = models.IntegerField(blank=True)
    order_date = models.DateField(blank=True, null=True)
    pay_date = models.DateField(blank=True, null=True)
    deliv_date = models.DateField(blank=True, null=True)
    state = models.CharField(max_length=10, choices=OrderState.choices, null=True)

    """def check_date(self, d):
        return (self.order_date == d)"""

    class Meta:
        managed = True
        db_table = 'orders'

    def __str__(self):
        return str(self.order_id) or ' '
