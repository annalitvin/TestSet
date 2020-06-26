from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from app import settings
from user_account.forms import UserAccountRegistrationForm, UserAccountProfileForm


class CreateUserAccountView(CreateView):
    model = settings.AUTH_USER_MODEL
    template_name = 'user_account/registration.html'
    form_class = UserAccountRegistrationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register new user'
        return context

    def get_success_url(self):
        return reverse('index')


class UserAccountLoginView(LoginView):
    template_name = 'user_account/login.html'
    extra_context = {'title': 'Login as a user'}


class UserAccountLogoutView(LogoutView):
    template_name = 'user_account/logout.html'
    extra_context = {'title': 'Logout'}


class UserAccountProfileView(SuccessMessageMixin, UpdateView):
    template_name = 'user_account/profile.html'
    extra_context = {'title': 'Edit current user profile'}
    form_class = UserAccountProfileForm

    success_url = reverse_lazy('account:profile')
    success_message = "Your account has been updated!"

    def get_object(self, queryset=None):
        return self.request.user
