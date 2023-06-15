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
    # template_name='man/man.html'


    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()

            Yandex_mail: str = settings.EMAIL_HOST_USER
            send_mail(
                'Код подтверждения',
                '1111',
                Yandex_mail,
                [form.cleaned_data['email']],
                fail_silently=False,
            )

        return super().form_valid(form)



