from django.db.models import Q, QuerySet
from django.views.generic import DetailView, ListView, TemplateView
from rest_framework import viewsets

from .models import Category, Product
from .serializers import ProductSerializer


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.filter(is_active=True)[:5]  # 5 активных продуктов для главной
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'
    
    def get_paginate_by(self, queryset):
        try:
            per_page = int(self.request.GET.get('per_page', 5))
            if per_page in [5, 10, 20, 50]:
                return per_page
        except ValueError:
            pass
        return 5

    def get_queryset(self) -> QuerySet[Product]:
        queryset = Product.objects.filter(is_active=True).select_related('category')

        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )

        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        sort = self.request.GET.get('sort', 'popular')
        if sort == 'price':
            queryset = queryset.order_by('price')
        elif sort == 'name':
            queryset = queryset.order_by('name')
        else:  # popular / default
            queryset = queryset.order_by('-id')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        context['search_query'] = self.request.GET.get('search')
        context['current_sort'] = self.request.GET.get('sort', 'popular')
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


class GuidesRecipesView(TemplateView):
    template_name = 'guides-recipes.html'


class ProductViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт для просмотра и поиска товаров.
    """
    serializer_class = ProductSerializer
    filterset_fields = ['category', 'price']
    search_fields = ['name', 'description']

    def get_queryset(self) -> QuerySet[Product]:
        return Product.objects.filter(is_active=True).select_related('category')
