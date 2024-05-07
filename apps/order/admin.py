from django.contrib import admin
from .models import Sevimlilar, Order
# Register your models here.


@admin.register(Sevimlilar)
class SevimlilarAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']
    list_filter = ['user', 'product']
    search_fields = ['user', 'product']
    list_per_page = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']
    list_filter = ['user', 'product']
    search_fields = ['user', 'product']
    list_per_page = 10