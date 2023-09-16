from django.test import TestCase
from django.urls import reverse

from account.forms import SignUpFormWithRusError
from account.models import CustomUser


class RegisterTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('_login')
        self.user_success = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password1': '7is-W2p-Pg7-xtx',
            'password2': '7is-W2p-Pg7-xtx',
        }
        self.user_short_password = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password1': 'tes',
            'password2': 'tes',
        }
        self.user_too_common_password = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password1': 'Password123',
            'password2': 'Password123',
        }

        self.user_unmatching_password = {
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password1': '7is-W2p-Pg7-xtx',
            'password2': '7is-W2p-Pg7-xt',
        }
        self.user_invalid_email = {
            'email': 'test.com',
            'username': 'username',
            'password1': '7is-W2p-Pg7-xtx',
            'password2': '7is-W2p-Pg7-xtx',
        }
        return super().setUp()

    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_can_register_user(self):
        form = SignUpFormWithRusError(self.user_success)
        self.assertTrue(form.is_valid())

    def test_cant_register_user_with_short_password(self):
        form = SignUpFormWithRusError(self.user_short_password)
        self.assertFalse(form.is_valid())

    def test_cant_register_user_with_too_common_password(self):
        form = SignUpFormWithRusError(self.user_too_common_password)
        self.assertFalse(form.is_valid())

    def test_cant_register_user_with_unmatching_passwords(self):
        form = SignUpFormWithRusError(self.user_unmatching_password)
        self.assertFalse(form.is_valid())

    def test_cant_register_user_with_invalid_email(self):
        form = SignUpFormWithRusError(self.user_invalid_email)
        self.assertFalse(form.is_valid())


class LoginTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('_login')
        self.user_success = {
            'username': 'username',
            'password': '7is-W2p-Pg7-xtx'
        }
        self.user_cantlogin_with_no_username = {
            'username': '',
            'password': 'tes',
        }
        self.user_cantlogin_with_no_password = {
            'username': 'username',
            'password': '',
        }
        self.user = CustomUser.objects.create_user(**{
            'email': 'testemail@gmail.com',
            'username': 'username',
            'password': '7is-W2p-Pg7-xtx',
        })
        return super().setUp()

    def test_can_access_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_success(self):
        response = self.client.login(**self.user_success)
        self.assertTrue(response)

    def test_cantlogin_with_no_username(self):
        response = self.client.login(**self.user_cantlogin_with_no_username)
        self.assertFalse(response)

    def test_cantlogin_with_no_password(self):
        response = self.client.login(**self.user_cantlogin_with_no_password)
        self.assertFalse(response)
