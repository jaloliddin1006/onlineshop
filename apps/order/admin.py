from django.contrib import admin
from .models import Sevimlilar
# Register your models here.


@admin.register(Sevimlilar)
class SevimlilarAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']
    list_filter = ['user', 'product']
    search_fields = ['user', 'product']
    list_per_page = 10