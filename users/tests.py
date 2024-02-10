# python manage.py test users.tests.UserRegistrationViewTestCase.test_user_registration_get
from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User

# Create your tests here.


class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.data = {
            'first_name': 'erbolat', 'last_name': 'ssabay',
            'username': 'erbolat', 'email': 'email@gmail.com',
            'password': 'Parol12345', 'password2': 'Parol12345',
        }
        self.path = reverse('users:registration')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Proactive - Регистрация')
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        # # check user creating
        # self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # self.assertRedirects(response, reverse('users:login'))
        # self.assertTrue(User.objects.filter(username=username).exists())

        # check email verification creating
        # email_verification = EmailVerification.objects.filter(user__username=username)
        # self.assertEqual(
        #     email_verification.first().expiration.date(),
        #     (now() + timedelta(hours=48)).date()
        # )

    def test_user_registration_post_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)
