from django.urls import path
from authapp.views import UserRegistrationView, UserLoginView

app_name = 'authapp'

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
]