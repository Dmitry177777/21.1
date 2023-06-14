from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from django.views.generic import CreateView
from main.forms import FormStyleMixin
from users.models import User
from django.core.mail import send_mail

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



    def send_order_email(self):
        send_mail(
            'Код подтверждения',
            '1111',
            'from@example.com',
            [self.user],
            fail_silently=False,
        )


    # def __init__ (self, *args, **kwargs):
    #     super(UserForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['password'].widget = forms.HiddenInput()