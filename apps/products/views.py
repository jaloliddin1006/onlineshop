from django.shortcuts import render
from django.views import View
from apps.products.models import Product


class HomePageView(View):
    def get(self, request):
        products = Product.objects.all().filter(is_active=True)
        featured_products = products.order_by('?')[:16]
        context = {
            'featured_products': featured_products,

        }
        return render(request, 'products/index.html', context)
