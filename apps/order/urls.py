from django.urls import path
from .views import AddToFavorite

urlpatterns = [
    path('add_to_favorite/', AddToFavorite.as_view(), name='add_to_favorite'),
]

