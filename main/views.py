import random

from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from main.forms import ProductForm, VersionForm
from main.models import Product, Category, Blog, Version


# Create your views here.


class index(ListView):
    model = Product
    extra_context = {
        'title': 'Первые продукты'
    }

    # Метод переопределяет представление и выводит только продукты с атрибутом (is_active=True)
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset[:6]


class CategoryListView(ListView):
    model = Category
    extra_context = {
        'title': 'Список категорий'
    }


class ProductListView(ListView):
    model = Product
    extra_context = {
        'title': 'Список продуктов'
    }

    # Метод переопределяет представление и выводит только продукты с атрибутом is_active=True)
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = context_data['object'].product_name
        return context_data


class ProductCreateView(CreateView):
    model = Product
    # fields = ('product_category', 'product_name', 'description', 'product_price',)
    form_class = ProductForm
    success_url = reverse_lazy('main:product_list')


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'main\product_form_with_formset.html'
    # fields = ('product_category', 'product_name', 'description', 'product_price',)
    form_class = ProductForm
    success_url = reverse_lazy('main:product_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST) # Обработка и сохранение POST запроса если он есть
        else:
            context_data['formset'] = VersionFormset()
        return context_data



class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('main:product_list')


class BlogListView(ListView):
    model = Blog
    extra_context = {
        'title': 'Список постов'
    }

    # Метод переопределяет представление и выводит только продукты с атрибутом is_active=True)
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_publication=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog
    success_url = reverse_lazy('main:blog_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = context_data['object'].message_heading
        return context_data

    # Обновлени счетчика просмотрове
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Обновлени счетчика просмотрове
        self.object.views_count += 1
        # запись изменений
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class BlogCreateView(CreateView):
    model = Blog
    fields = ('message_heading', 'message_content', 'message_preview', 'is_publication',)
    success_url = reverse_lazy('main:blog_list')


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('message_heading', 'message_content', 'message_preview', 'is_publication',)

    # Получаем данные объекта и выводим ту же страницу
    def get_success_url(self) -> str:
        return reverse_lazy('main:blog_update', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('main:blog_list')

# class UsersListView(ListView):
#     model=Users
#     extra_context = {
#         'title': 'Список пользователей'
#     }
