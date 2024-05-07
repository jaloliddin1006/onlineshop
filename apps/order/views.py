from django.shortcuts import render, redirect

from apps.products.models import Product
from .models import Sevimlilar
from django.views import View
# Create your views here.


class AddToFavorite(View):
    def post(self, request):
        user = request.user
        print(request.POST)
        product = request.POST.get('product_id')
        product = Product.objects.get(id=product)
        Sevimlilar.objects.create(user=user, product=product)
        return redirect('detail', uuid=product.id)