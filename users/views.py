import os

import requests
from django.contrib.auth.forms import UserChangeForm
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from config import settings
from users.forms import UserForm, UserRegisterForm
from users.models import User


class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
# Create your views here.


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('main:index')
    # template_name=('users:man')


    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()

            data ={
                'email': form.cleaned_data['email'],
                'message': 'Подтвердите регистрацию'

            }


            html_body = render_to_string("users/message_registr.html", data)
            msg=EmailMultiAlternatives(subject="Регистрация", to=[form.cleaned_data["email"]])
            msg.attach_alternative(html_body, "text/html")
            msg.send()


            # send_mail(
            #     'Подтвержднение регистрации',
            #     'Код подтверждения 1111',
            #     settings.EMAIL_HOST_USER,
            #     [form.cleaned_data["email"]],
            #     fail_silently=False,
            # )

        return super().form_valid(form)



