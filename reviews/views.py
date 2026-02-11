from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from products.models import Product

from .forms import ReviewForm
from .models import Review


class CreateReviewView(LoginRequiredMixin, View):
    """Handle review creation with purchase verification."""

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)

        # Check if user has purchased this product
        if not Review.user_has_purchased(request.user, product):
            messages.error(request, "You can only review products you have purchased.")
            return redirect('products:product_detail', slug=product.slug)

        # Check if user already reviewed this product
        if Review.objects.filter(user=request.user, product=product).exists():
            messages.warning(request, "You have already reviewed this product.")
            return redirect('products:product_detail', slug=product.slug)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, "Thank you for your review!")
        else:
            messages.error(request, "Please provide a valid rating (1-5) and review text.")

        return redirect('products:product_detail', slug=product.slug)
