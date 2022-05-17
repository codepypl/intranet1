from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext as _
from django.core.mail import send_mail
from passlib.hash import sha512_crypt


from .managers import AccountManager


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email_password = models.CharField(_('mail_password'), max_length=255, default='')

    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_manager = models.BooleanField(_('is_manager'), default=False)

    objects = AccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    def get_full_name(self):
        """
        Zwraca imie i nazwisko konta
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Zwraca imię pracownika
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Wysyła e-mail do pracownika
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def create_email_password(self, password):
        """
            Hashowanie hasła kompatybilnego z Dovecot
        """
        algo = "{SHA512-CRYPT}"
        if not self.email_password.startswith("%s$6$" % algo):
            salt = sha512_crypt.salt
            self.email_password = "{algo}{crypted}".format(
                algo=algo,
                crypted=sha512_crypt.using(rounds=5000, salt=salt).hash(password)
            )
