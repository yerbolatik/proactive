import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

# Create your models here.


class User(AbstractUser):
    image = models.ImageField(upload_to='user_images', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f"EmailVerification object for {self.user.email}"

    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={
                       "email": self.user.email, "code": self.code})
        verification_link = f"{settings.DOMAIN_NAME}{link}"
        subject = f"Подтверждение учетной записи для {self.user.username}"
        message = f"Для подтвеждения учетной записи для {
            self.user.email} перейдите по ссылке: {verification_link}"

        # Создаем сообщение MIME
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_HOST_USER
        msg['To'] = self.user.email
        msg['Subject'] = subject

        # Добавляем текст сообщения
        msg.attach(MIMEText(message, 'plain'))

        try:
            # Создаем SMTP сервер и отправляем сообщение
            with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                server.login(settings.EMAIL_HOST_USER,
                             settings.EMAIL_HOST_PASSWORD)
                server.sendmail(settings.EMAIL_HOST_USER,
                                self.user.email, msg.as_string())
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")

        # try:
        #     # Используем send_mail для отправки сообщения
        #     send_mail(
        #         subject=subject,
        #         message=message,
        #         from_email=settings.EMAIL_HOST_USER,
        #         recipient_list=[self.user.email],
        #         fail_silently=False,
        #     )
        # except Exception as e:
        #     print(f"Ошибка при отправке сообщения: {e}")

    def is_expired(self):
        return True if now() >= self.expiration else False
