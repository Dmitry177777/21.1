from datetime import date

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

NULLABLE = {'blank':True, 'null': True}
class Product(models.Model):

    product_name = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.CharField(max_length=150, verbose_name='Описание')
    product_image = models.ImageField(upload_to='product_image/', verbose_name='Изображение', **NULLABLE)
    product_category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Категория')
    product_price = models.IntegerField(default=None,verbose_name='Цена за покупку', **NULLABLE)
    date_of_creation = models.DateField(default=date.today, verbose_name='Дата создания')
    date_of_change = models.DateField(default=date.today, verbose_name='Дата последнего изменения')
    is_active = models.BooleanField(default=True, verbose_name='Есть на складе')

    def __str__(self):
        return f'{self.product_name} : {self.description} : {self.product_image} {self.product_category} {self.product_price} {self.date_of_creation} {self.date_of_change}'


# функция переопределяет удаление и не удаляет объект а переводит флаг is_active = False
    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()


    class Meta:
        verbose_name='продукция'
        verbose_name_plural='продукции'
        ordering = ('product_category', )

class Category(models.Model):
    product_category = models.CharField(max_length=150, verbose_name='Наименование')
    description = models.CharField(max_length=150, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активные категории')

    def __str__(self):
        return f'{self.product_category} : {self.description}'

    class Meta:
        verbose_name='категория'
        verbose_name_plural='категории'
        ordering = ('product_category', )



class Blog(models.Model):
    slug = models.CharField(max_length=250, null=False, unique=True, verbose_name='slug')
    message_preview = models.ImageField(upload_to='message_preview/', verbose_name='Превью', **NULLABLE)
    message_heading = models.CharField(max_length=250, verbose_name='Заголовок')
    message_content= models.TextField(verbose_name='Контент', **NULLABLE)
    date_of_creation = models.DateField(default=date.today, verbose_name='Дата создания')
    date_of_change = models.DateField(default=date.today, verbose_name='Дата последнего изменения')
    is_publication = models.BooleanField(default=True, verbose_name='Опубликовано')
    views_count = models.IntegerField(default=0,verbose_name='Количество просмотров')
    user_name = models.CharField(max_length=250,  **NULLABLE, verbose_name='Пользователи')



    def __str__(self):
        return f'{self.message_heading} : {self.message_content}'

        # функция переопределения slug
    def get_absolute_url(self):
        return reverse('blog_item', kwargs={'slug': self.slug})  # new


    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.message_heading)
            self.save()
        return super().save(*args, **kwargs)




    # функция переопределяет удаление и не удаляет объект а переводит флаг is_publication = False
    def delete(self, *args, **kwargs):
            self.is_publication = False
            self.save()

    class Meta:
        verbose_name='Запись блога'
        verbose_name_plural='Записи блога'
        ordering = ('message_heading', )


# class Users(models.Model):
#     user_name = models.CharField(max_length=150, verbose_name='Имя')
#     user_lastname = models.CharField(max_length=150, verbose_name='Отчество')
#     user_surname = models.CharField(max_length=150, verbose_name='Фамилия')
#     user_email = models.EmailField(verbose_name='email', unique=True)
#
#     def __str__(self):
#         return f'{self.user_name} : {self.user_lastname} : {self.user_surname} : {self.user_email}'
#
#     class Meta:
#         verbose_name = 'Пользователь'
#         verbose_name_plural = 'Пользователи'
#         ordering = ('user_name',)
