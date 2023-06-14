import os

from django.contrib.auth.forms import UserChangeForm
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

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

    def get_object(self, queryset=None):
        self.send_order_email()
        return self.request.user

    def send_order_email(self):
        Yandex_mail: str = os.getenv('Yandex_mail')
        send_mail(
            'Код подтверждения',
            '1111',
            Yandex_mail,
            [self.request.user.email],
            fail_silently=False,
        )
        return send_mail



