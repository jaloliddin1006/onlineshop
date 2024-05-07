from django.shortcuts import render, redirect

from apps.products.models import Product
from .models import Sevimlilar, Order
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
    

class FavoriteView(View):
    def get(self, request):
        user = request.user
        sevimlilar = Sevimlilar.objects.filter(user=user)
        context = {
            'sevimlilar': sevimlilar
        }
        return render(request, 'products/shop-wishlist.html', context)

def delete_favourite(request, uuid):
    sevimlilar = Sevimlilar.objects.get(id=uuid)
    sevimlilar.delete()
    return redirect('favorite')

def add_shop_card(request, uuid):
    url = request.META.get('HTTP_REFERER')
    user = request.user
    product = Product.objects.get(id=uuid)
    Order.objects.create(user=user, product=product)
    return redirect(url)