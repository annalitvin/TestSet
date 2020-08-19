from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, FormView

from django.conf import settings
from user_account.forms import UserAccountRegistrationForm, UserAccountProfileForm, ContactUs


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


class UserAccountLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'user_account/logout.html'
    extra_context = {'title': 'Logout'}

    login_url = reverse_lazy('account:login')


class UserAccountProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'user_account/profile.html'
    extra_context = {'title': 'Edit current user profile'}
    form_class = UserAccountProfileForm

    success_url = reverse_lazy('account:profile')
    success_message = "Your account has been updated!"

    login_url = reverse_lazy('account:login')

    def get_object(self, queryset=None):
        return self.request.user


class ContactUsView(FormView):
    template_name = 'user_account/contact_us.html'
    extra_context = {'title': 'Send us a message!'}
    success_url = reverse_lazy('index')
    form_class = ContactUs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        user_email = request.user.email

        if form.is_valid():
            send_mail(
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'] + f" {user_email}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
