from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'class': 'rating-input',
            'placeholder': 'Rating (1-5)'
        })
    )
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'review-textarea',
            'placeholder': 'Share your experience with this product...',
            'rows': 4
        })
    )

    class Meta:
        model = Review
        fields = ['rating', 'text']
