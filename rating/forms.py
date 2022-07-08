from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.forms import widgets
from django.forms.widgets import Widget
from .models import BusinessRating, ProductRating

User = get_user_model()


class BusinessRatingForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(), label='')
    class Meta:
        model = BusinessRating
        fields = [
            'rating',
            'content',
        ]


class ProductRatingForm(forms.ModelForm):
    class Meta:
        model = ProductRating
        fields = [
            'rating',
            'content',
        ]
