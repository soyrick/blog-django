from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm, EmailAuthenticationForm


class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = EmailAuthenticationForm


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('blog:post_list')
    http_method_names = ['get', 'post', 'options']

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
