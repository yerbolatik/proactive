from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from users.views import password_reset_request

from django.urls import path

from users.views import (EmailVerificationView, UserLoginView, UserProfileView,
                         UserRegistrationView)

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/<int:pk>', login_required(UserProfileView.as_view()), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/<str:email>/<uuid:code>/',
         EmailVerificationView.as_view(), name='email_verification'),
    path('password_reset/', password_reset_request, name='password_reset'),

]
