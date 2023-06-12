from django import forms
from django.views.generic import  CreateView, UpdateView
from main.models import Product, Version


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        #fields = ('','')
        #exclude = ('','')

class VersionForm(forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'

