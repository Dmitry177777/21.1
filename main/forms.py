from django import forms
from django.views.generic import CreateView, UpdateView
from main.models import Product, Version

exclusion_list = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        #fields = ('','')
        #exclude = ('','')

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_product_name (self):
        cleaned_data = self.cleaned_data['product_name']
        for i in exclusion_list:
            if i.lower() in cleaned_data.lower():
                raise forms.ValidationError('Недопустимые слова в наименовании: казино, криптовалюта, крипта, биржа, дешево, бесплатно, обман, полиция, радар')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        for i in exclusion_list:
            if i.lower() in cleaned_data.lower():
                raise forms.ValidationError(
                    'Недопустимые слова в описании: казино, криптовалюта, крипта, биржа, дешево, бесплатно, обман, полиция, радар')

        return cleaned_data



class VersionForm(forms.ModelForm):

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



    class Meta:
        model = Version
        fields = '__all__'

