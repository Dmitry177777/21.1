from django.contrib.auth.forms import UserChangeForm
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
        return self.request.user


    def form_valid(self, form):
        send_order_email()

        return super().form_valid(form)