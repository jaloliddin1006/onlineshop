from django.urls import path
from .views import HomePageView, ShopAllView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('shop/', ShopAllView.as_view(), name='shop'),
]