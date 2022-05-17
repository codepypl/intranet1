
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .forms import AccountCreationForm, ChangeEmailPasswordForm
from django.contrib.auth.views import PasswordChangeView


class CreateUserView(CreateView):
    form_class = AccountCreationForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('login')


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = ChangeEmailPasswordForm
    success_url = reverse_lazy('konto:home')
    template_name = 'account/change_email_password.html'
    title = 'x'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        print(kwargs['user'])
        print(self.success_url)
        return kwargs

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)
