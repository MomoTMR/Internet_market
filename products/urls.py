from django.urls import path
from .views import HomeView, ProductListView, ProductDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),                                          # Главная
    path('products/', ProductListView.as_view(), name='products'),                      # Список продуктов
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),  # Детали по slug
]
