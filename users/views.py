from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import UpdateView, CreateView
from users.forms import UserForm, UserRegisterForm
from users.models import User
from django.contrib.auth.tokens import default_token_generator as \
    token_generator
from django.shortcuts import render, redirect




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
        return render(request, RegisterView.template_name, context)


    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get ('password1')
            user = User.objects.create_user(email=email, password=password)
            RegisterView.send_email_for_verify(self, request, user)
            return redirect('users:confirm_email')

        context = {
            'form': form,
           }
        return render(request, RegisterView.template_name, context)

    def send_email_for_verify(self, request, user, ):
        current_site = get_current_site(request)
        context = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_generator.make_token(user),
            'link_message': "Пожалуйста перейдите по ссылке чтобы закончить регистрацию",
        }
        message = render_to_string(
            'users/verify_email.html',
            context=context,
        )
        email = EmailMessage(
            'Veryfi email',
            message,
            to=[user.email],
        )
        email.send()


