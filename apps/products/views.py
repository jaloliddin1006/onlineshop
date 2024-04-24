from django.shortcuts import render
from django.views import View
from apps.products.models import Product
from django.core.paginator import Paginator

class HomePageView(View):
    def get(self, request):
        products = Product.objects.all().filter(is_active=True)
        featured_products = products.order_by('?')[:16]
        context = {
            'featured_products': featured_products,

        }
        return render(request, 'products/index.html', context)


class ShopAllView(View):
    def get(self, request):
        products = Product.objects.all().filter(is_active=True)

        page_size = request.GET.get('page_size', 10)
        paginator = Paginator(products, page_size)

        page = request.GET.get('page', 1)
        page_obj = paginator.get_page(page)

        context = {
            'products': page_obj,
            'page_size': page_size
        }

        return render(request, 'products/shop.html', context)