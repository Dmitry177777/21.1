from django import forms
from django.views.generic import  CreateView, UpdateView
from main.models import Product

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        #fields = ('','')
        #exclude = ('','')

