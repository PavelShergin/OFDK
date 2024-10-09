import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')
django.setup()



from http import HTTPStatus
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.forms import UserRegistrationForm
from users.models import User, EmailVerification


class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.data = {
            'first_name': 'Pavell', 'last_name': 'Shergin',
            'username': 'Pavell', 'email': 'tapok772oe3@mail.ru',
            'password1': '123445678pP', 'password2': '123445678pP',
        }

        self.path = reverse('users:registration')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        #self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Регистрация')
        #self.assertTemplateUsed(response, 'user/registration.html')

    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertTrue(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        # check creating of user
        #self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username)).exists()

        # check creating of email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        #self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)

