from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseForbidden
from django.shortcuts import HttpResponseRedirect, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin
from baskets.models import Basket
from users.forms import (UserLoginForm, UserProfileForm,
                         UserRegistrationForm)
from users.models import User, EmailVerification


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Proactive - Авторизация'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрированы'
    title = 'Proactive - Регистрация'


def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            # Проверяем, есть ли пользователь с указанным адресом электронной почты
            email = form.cleaned_data.get('email')
            users = User.objects.filter(email=email)
            if users.exists():
                # Если пользователь найден, отправляем письмо для сброса пароля
                form.save(
                    request=request,
                    from_email=settings.EMAIL_HOST_USER,
                    email_template_name='registration/password_reset_email.html'
                )
                messages.success(
                    request,
                    "Инструкции по сбросу пароля отправлены на ваш адрес электронной почты."
                )
            else:
                # Если пользователь не найден, выводим сообщение об ошибке
                messages.error(request, "Пользователь с указанным адресом электронной почты не найден.")
                return redirect('users:login')
    else:
        form = PasswordResetForm()
    return render(request, "users/password_reset.html", {"form": form})


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Proactive - Профиль'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        context['baskets'] = baskets
        return context

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.kwargs['pk']})

    def dispatch(self, request, *args, **kwargs):
        # Получить идентификатор пользователя, который отправил запрос на редактирование профиля
        user_id = kwargs.get("pk")

    # # Проверить, авторизован ли текущий пользователь, и имеет ли он право редактировать этот профиль
        if not self.request.user.is_authenticated or self.request.user.id != user_id:
            return HttpResponseForbidden("У вас нет прав на редактирование этого профиля")

        return super().dispatch(request, *args, **kwargs)


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Proactive - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(
            user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
