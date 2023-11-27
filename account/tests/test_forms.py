from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from account.forms import CustomUserSignUpForm, CustomUserUpdateForm
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
        self.user_not_unique_email = {
            'email': 'testemail@gmail.com',
            'username': 'username1',
            'password1': '7is-W2p-Pg7-xtx',
            'password2': '7is-W2p-Pg7-xtx',
        }
        self.user_not_unique_username = {
            'email': 'testemail1@gmail.com',
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
        form = CustomUserSignUpForm(self.user_success)
        self.assertTrue(form.is_valid())

    def test_cant_register_user_with_not_unique_email(self):
        form = CustomUserSignUpForm(self.user_success)
        form.save()
        form1 = CustomUserSignUpForm(self.user_not_unique_email)
        self.assertFalse(form1.is_valid())

    def test_cant_register_user_with_not_unique_username(self):
        form = CustomUserSignUpForm(self.user_success)
        form.save()
        form1 = CustomUserSignUpForm(self.user_not_unique_username)
        self.assertFalse(form1.is_valid())

    def test_cant_register_user_with_short_password(self):
        form = CustomUserSignUpForm(self.user_short_password)
        self.assertFalse(form.is_valid())

    def test_cant_register_user_with_too_common_password(self):
        form = CustomUserSignUpForm(self.user_too_common_password)
        self.assertFalse(form.is_valid())

    def test_cant_register_user_with_unmatching_passwords(self):
        form = CustomUserSignUpForm(self.user_unmatching_password)
        self.assertFalse(form.is_valid())

    def test_cant_register_user_with_invalid_email(self):
        form = CustomUserSignUpForm(self.user_invalid_email)
        self.assertFalse(form.is_valid())


class LoginTest(TestCase):
    def setUp(self):
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


class CustomUserUpdateFormTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='existing_user',
            email='existing@example.com',
            password='password123'
        )
        self.form_data = {
            'username': 'new_user',
            'email': 'new@example.com',
            'bio': 'This is a test bio',
            'avatar': None,
        }

    def test_clean_email(self):
        form = CustomUserUpdateForm(data=self.form_data, instance=self.user)
        self.assertTrue(form.is_valid())

        # Create a new user with the same email
        duplicate_user = get_user_model().objects.create_user(
            username='duplicate_user',
            email='new@example.com',
            password='password456'
        )

        form = CustomUserUpdateForm(data=self.form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'][0], 'Email адрес должен быть уникальным')

    def test_unique_username(self):
        form = CustomUserUpdateForm(data=self.form_data, instance=self.user)
        self.assertTrue(form.is_valid())

        # Create a new user with the same username
        duplicate_user = get_user_model().objects.create_user(
            username='new_user',
            email='another@example.com',
            password='password789'
        )

        form = CustomUserUpdateForm(data=self.form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertEqual(form.errors['username'][0], 'Пользователь с таким именем уже существует.')
