from django.urls import path
from .views import CreateUserView, CustomPasswordChangeView
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

app_name = 'konto'

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('logowanie/', auth_views.LoginView.as_view(template_name='account/login.html'), name='logowanie'),
    path('zmien-haslo/', CustomPasswordChangeView.as_view(), name='zmien-haslo'),
    path('wyloguj/', auth_views.LogoutView.as_view(), name='wyloguj'),
]
