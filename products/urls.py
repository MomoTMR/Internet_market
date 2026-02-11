from django.urls import path

from .views import GuidesRecipesView, ProductDetailView, ProductListView

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='products'),                # Список продуктов
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),  # Детали по slug
    path('guides-recipes/', GuidesRecipesView.as_view(), name='guides_recipes'),        # Руководства и рецепты
]
