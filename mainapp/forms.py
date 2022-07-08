from cProfile import label
from django import forms
from .models import Business, Product, BusinessPost, BusinessPostComment, PostCategory


class BusinessCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=100, label='Business name')
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':3, 'cols':3, 'maxlength': '1000', 'style':'resize:none;'}), help_text='Write a description about your business. This could include the services you offer.', max_length=200)
    opening_hours_from = forms.CharField(label='From')
    opening_hours_to = forms.CharField(label='To')
    
    class Meta:
        model = Business
        fields = [
            'name',
            'category',
            'description',
            'opening_hours_from',
            'opening_hours_to',
        ]

class BusinessThumbnailForm(forms.ModelForm):
    phone = forms.CharField(label='Phone number')
    low_thumbnail = forms.ImageField(required=False)
    class Meta:
        model = Business
        fields = [
            'phone',
            'thumbnail',
        ]


class BusinessThumbnailForm2(forms.ModelForm):
    low_thumbnail = forms.ImageField(required=False)
    class Meta:
        model = Business
        fields = [
            'thumbnail',
        ]


class ProductForm(forms.ModelForm):
    price = forms.CharField(label='Price (optional)', required=False)
    low_image = forms.ImageField(required=False)
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'image',
            'price',
        ]

class BusinessEditForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows':5, 'cols':3, 'style':'resize:none;'}), help_text='Write a description about your business. This could include the services you offer.', max_length=1000)
    opening_hours_from = forms.CharField(label='From')
    opening_hours_to = forms.CharField(label='To')
    show_location = forms.BooleanField(label='Allow people to get directions to your primary location', required=False)
    class Meta:
        model = Business
        fields = [
            'name',
            'category',
            'description',
            'opening_hours_from',
            'opening_hours_to',
            'show_location',
        ]
class BusinessPersonalInfoEditForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = [
            'email',
            'phone'
        ]

class CreateBusinessPost(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=PostCategory.objects.all(), label='Choose post type')
    content = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = BusinessPost
        fields = [
            'category',
            'content',
        ]
        
class BusinessPostCommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, label='')
    class Meta:
        model = BusinessPostComment
        fields = [
            'content'
        ]