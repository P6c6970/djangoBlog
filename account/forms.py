from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


# для admin
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')


# для admin
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeFormRus(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input_text', })  # изменяет параметры поля ввода
        self.fields['email'].widget.attrs.update({'class': 'input_text', })  # изменяет параметры поля ввода

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class SignUpFormWithRusError(UserCreationForm):
    def __init__(self, *args, **kwargs):
        self.error_messages['password_mismatch'] = 'Пароли не совпадают!'
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input_text', })  # изменяет параметры поля ввода
        self.fields['password1'].widget.attrs.update({'class': 'input_text', })  # изменяет параметры поля ввода
        self.fields['password2'].widget.attrs.update({'class': 'input_text', })  # изменяет параметры поля ввода

    email = forms.EmailField(max_length=200, help_text='Required',
                             widget=forms.TextInput(attrs={'class': 'input_text'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


from django.contrib.auth.forms import AuthenticationForm


class AuthFormWithRusError(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'Неверный логин или пароль!'
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input_text', })  # изменяет параметры поля ввода
        self.fields['password'].widget.attrs.update({'class': 'input_text', })  # изменяет параметры поля ввода


from django.contrib.auth.forms import PasswordResetForm


class UserForgotPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'input_text', })  # изменяет параметры поля ввода

    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class': 'input_text'}))

    class Meta:
        fields = ("username", "email")


from django.contrib.auth.forms import SetPasswordForm


class MySetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'input_text', })  # изменяет параметры поля ввода
        self.fields['new_password2'].widget.attrs.update({'class': 'input_text', })  # изменяет параметры поля ввода
