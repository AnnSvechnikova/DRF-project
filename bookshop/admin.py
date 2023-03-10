from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Book, Order, User


@admin.register(Book)
class ClassesAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'title', 'in_stock', 'descr', 'price', 'picture')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'password', 'full_name', 'is_staff', 'is_superuser')


@admin.register(Order)
class PurchasesAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user_id', 'book_id', 'amount', 'order_date', 'pay_date',  'deliv_date', 'state')
# Register your models here.