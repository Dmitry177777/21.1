from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from users.forms import UserForm
from users.models import User


class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
# Create your views here.
