
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import UpdateView, CreateView
from users.forms import UserForm, UserRegisterForm
from users.models import User
from django.contrib.auth.tokens import default_token_generator as \
    token_generator
from django.shortcuts import render, redirect
from users.utils import send_email_for_verify



class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
# Create your views here.

class EmailVerify(CreateView):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('home')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    # success_url = reverse_lazy('main:index')
    template_name = 'users/user_form.html'

    def get(self, request):
        context = {
            'form': UserRegisterForm()
        }
        return render(request, self.template_name, context)


    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            # message = 'Подтвердите регистрацию'
            password = form.cleaned_data.get ('password1')
                        
            user = authenticate(email=email, password=password)
            send_email_for_verify(request, user)
            return redirect('confirm_email')

        context = {
            'form': form
        }
        return render(request, self.template_name, context)





