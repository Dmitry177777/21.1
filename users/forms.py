from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from django.views.generic import CreateView
from main.forms import FormStyleMixin
from users.models import User
from django.core.mail import send_mail
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from users.utils import send_email_for_verify

User = get_user_model()

class UserForm (FormStyleMixin,UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar')

    def __init__ (self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()

class UserRegisterForm (FormStyleMixin,UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )
            if not self.user_cache.email_verify:
                send_email_for_verify(self.request, self.user_cache)
                raise ValidationError(
                    'Email not verify, check your email',
                    code='invalid_login',
                )

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data




    # def __init__ (self, *args, **kwargs):
    #     super(UserForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['password'].widget = forms.HiddenInput()