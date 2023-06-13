from django.contrib.auth.forms import UserChangeForm
from django.views.generic import UpdateView

from users.models import User


class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserChangeForm

    def get_object(self, queryset=None):
        return self.request.user
# Create your views here.
