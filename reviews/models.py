from django.conf import settings
from django.db import models

from products.models import Product

User = settings.AUTH_USER_MODEL


class Review(models.Model):
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['product', 'user']
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating}/5"

    @staticmethod
    def user_has_purchased(user, product):
        """Check if user has purchased this product."""
        from orders.models import OrderItem
        return OrderItem.objects.filter(
            order__user=user,
            product=product
        ).exists()
