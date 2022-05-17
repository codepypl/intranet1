from django import forms
from django.forms import PasswordInput
from django.utils.translation import gettext as _
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordChangeForm
from .models import Account


class AccountCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('haslo'), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_('Potwierdz_haslo'), widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ['email', 'first_name', 'last_name']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("haslo_nieidentyczne"))
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.create_email_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AccountChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('email', 'password', 'first_name', 'last_name',
                  'is_manager', 'is_active', 'is_staff')

    def clean_password(self):
        return self.initial["password"]


class ChangeEmailPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(required=True, label=_('stare_haslo'),
                                   widget=PasswordInput(attrs={
                                       'class': 'form-control'}),
                                   error_messages={
                                       'required': 'Το συνθηματικό δε μπορεί να είναι κενό'})

    new_password1 = forms.CharField(required=True, label='Συνθηματικό',
                                    widget=PasswordInput(attrs={
                                        'class': 'form-control'}),
                                    error_messages={
                                        'required': 'Το συνθηματικό δε μπορεί να είναι κενό'})
    new_password2 = forms.CharField(required=True, label='Συνθηματικό (Επαναλάβατε)',
                                    widget=PasswordInput(attrs={
                                        'class': 'form-control'}),
                                    error_messages={
                                        'required': 'Το συνθηματικό δε μπορεί να είναι κενό'})

    def clean_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError(_("haslo_nieidentyczne"))
        return new_password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["new_password2"])
        user.create_email_password(self.cleaned_data["new_password2"])
        if commit:
            user.save()
        return user


