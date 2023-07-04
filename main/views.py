import random
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from main.forms import ProductForm, VersionForm
from main.models import Product, Category, Blog, Version
from main.services import  get_product_category


# Create your views here.


class index(LoginRequiredMixin, ListView):
    model = Product
    extra_context = {
        'title': 'Первые продукты'
    }

    # Метод переопределяет представление и выводит только продукты с атрибутом (is_active=True)
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset[:6]




class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    extra_context = {
        'title': 'Список категорий'
    }


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    extra_context = {
        'title': 'Список продуктов'
    }

    # Метод переопределяет представление и выводит только продукты с атрибутом is_active=True)
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_active=True)
        return queryset


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = context_data['object'].product_name
        context_data['product_category'] = get_product_category(self.object)
        return context_data


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    template_name = 'main\product_form_with_formset.html'
    permission_required = "main.add_product"
    # fields = ('product_category', 'product_name', 'description', 'product_price',)
    form_class = ProductForm
    success_url = reverse_lazy('main:product_list')



    def get_context_data(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            # Обработка ошибки не авторизованных пользователей
            raise BaseException("Вы не авторизованы. Создавать продукты может только авторизованный пользователь.")
        else:
            context_data = super().get_context_data(**kwargs)
        return context_data

    def form_valid(self, form):

        form.instance.is_user_email = self.request.user.email  # запись авторизованного пользователя в шаблон
        form.save()
        return super().form_valid(form)



class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    template_name = 'main\product_form_with_formset.html'
    permission_required = "main.change_product"
    # fields = ('product_category', 'product_name', 'description', 'product_price',)
    form_class = ProductForm
    success_url = reverse_lazy('main:product_list')



    def get_context_data(self,  **kwargs):
        if not self.request.user.is_authenticated:
            # Обработка ошибки не авторизованных пользователей
            raise BaseException("Вы не авторизованы. Изменять продукты может только авторизованный пользователь.")
        else:
            if self.request.user.is_superuser or self.object.is_user_email == self.request.user.email: # проверка пользователя на автора или суперюзера
                context_data = super().get_context_data(**kwargs)
                VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
                if self.request.method == 'POST':
                    context_data['formset'] = VersionFormset(self.request.POST, instance=self.object) # Обработка и сохранение POST запроса если он есть
                else:
                    context_data['formset'] = VersionFormset(instance=self.object)
                    # Обработка ошибки не авторизованных пользователей

            else:
                raise BaseException("Вы не автор. Вы не администратор.")
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']

        self.object =form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        form.instance.is_user_email = self.request.user.email  # запись авторизованного пользователя в шаблон
        form.save()
        return super().form_valid(form)



class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('main:product_list')
    permission_required = "main.delete_product"

class BlogListView(LoginRequiredMixin, ListView):
    model = Blog
    extra_context = {
        'title': 'Список постов'
    }

    # Метод переопределяет представление и выводит только продукты с атрибутом is_active=True)
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_publication=True)
        return queryset


class BlogDetailView(LoginRequiredMixin, DetailView):
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


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Blog
    fields = ('message_heading', 'message_content', 'message_preview', 'is_publication',)
    success_url = reverse_lazy('main:blog_list')


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Blog
    fields = ('message_heading', 'message_content', 'message_preview', 'is_publication',)

    # Получаем данные объекта и выводим ту же страницу
    def get_success_url(self) -> str:
        return reverse_lazy('main:blog_update', kwargs={'pk': self.object.pk})


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('main:blog_list')

# class UsersListView(ListView):
#     model=Users
#     extra_context = {
#         'title': 'Список пользователей'
#     }