from django.shortcuts import render, get_object_or_404
from django.views import View
from apps.products.models import Product, Category
from django.core.paginator import Paginator
from django.db.models import Q


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


        sort_by = request.GET.get('sort_by', 'title')


        categories = Category.objects.all().filter(is_active=True, parent=None)
        products = Product.objects.all().filter(is_active=True).order_by(sort_by)


        search = request.GET.get('search', '')
        if search:
            products = products.filter(Q(title__icontains=search) | Q(description__icontains=search)).order_by(sort_by)

        page_size = request.GET.get('page_size', 10)
        if page_size == 'all':
            page_size = products.count()
        paginator = Paginator(products, page_size)

        page = request.GET.get('page', 1)
        page_obj = paginator.get_page(page)




        context = {
            'products': page_obj,
            'page_size': page_size,
            'categories': categories,
            'search': search
        }

        return render(request, 'products/shop.html', context)


class ShopCategoryView(View):
    def get(self, request, uuid):
        ctg = get_object_or_404(Category, id=uuid)
        print(ctg)
        categories = Category.objects.all().filter(is_active=True, parent=ctg)
        if not categories:
            categories = Category.objects.all().filter(is_active=True, level=1)

        ctg_products = ctg.products.filter(is_active=True).order_by('?')

        page_size = request.GET.get('page_size', 10)
        paginator = Paginator(ctg_products, page_size)

        page = request.GET.get('page', 1)
        page_obj = paginator.get_page(page)

        context = {
            'products': page_obj,
            'page_size': page_size,
            'categories': categories,

        }

        return render(request, 'products/shop.html', context)

