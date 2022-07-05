from django.contrib.gis import forms
from mainapp.models import Business

class MyGeoForm(forms.ModelForm):
    location = forms.PointField(
        widget=forms.OSMWidget()
    )
    class Meta:
        model = Business
        fields = ['location',]