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

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class SignUpFormWithRusError(UserCreationForm):
    def __init__(self, *args, **kwargs):
        self.error_messages['password_mismatch'] = 'Пароли не совпадают!'
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'id': "typeLoginX", 'class': "form-control form-control-lg"})  # изменяет параметры поля ввода
        self.fields['password1'].widget.attrs.update({'id': "typePassword1X", 'class': "form-control form-control-lg"})
        self.fields['password2'].widget.attrs.update({'id': "typePassword2X", 'class': "form-control form-control-lg"})

    email = forms.EmailField(max_length=200, help_text='Required',
                             widget=forms.TextInput(attrs={'id': "typeEmailX", 'class': "form-control form-control-lg"}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    # def __init__(self, *args, **kwargs):
    #     """
    #     Обновление стилей формы регистрации
    #     """
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields['username'].widget.attrs.update({"placeholder": 'Придумайте свой логин'})
    #         self.fields['email'].widget.attrs.update({"placeholder": 'Введите свой email'})
    #         self.fields['first_name'].widget.attrs.update({"placeholder": 'Ваше имя'})
    #         self.fields["last_name"].widget.attrs.update({"placeholder": 'Ваша фамилия'})
    #         self.fields['password1'].widget.attrs.update({"placeholder": 'Придумайте свой пароль'})
    #         self.fields['password2'].widget.attrs.update({"placeholder": 'Повторите придуманный пароль'})
    #         self.fields[field].widget.attrs.update({"class": "form-control", "autocomplete": "off"})


from django.contrib.auth.forms import AuthenticationForm


class AuthFormWithRusError(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        self.error_messages['invalid_login'] = 'Неверный логин или пароль!'
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'id': "typeLoginX", 'class': "form-control form-control-lg"})  # изменяет параметры поля ввода
        self.fields['password'].widget.attrs.update({'id': "typePasswordX", 'class': "form-control form-control-lg"})  # изменяет параметры поля ввода


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
