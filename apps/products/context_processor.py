from .models import Category

def category_context(request):
    categories = Category.objects.all().filter(is_active=True, parent=None)
    mega_menu = categories[:3]
    last_ctgs = Category.objects.all().filter(is_active=True, children__isnull=True)

    print(mega_menu)

    context = {
        'categories': categories,
        'mega_menu': mega_menu,
        'last_ctgs': last_ctgs
    }

    return context