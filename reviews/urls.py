from django.urls import path

from .views import CreateReviewView

app_name = 'reviews'

urlpatterns = [
    path('create/<int:product_id>/', CreateReviewView.as_view(), name='create_review'),
]
