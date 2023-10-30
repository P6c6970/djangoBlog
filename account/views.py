# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.decorators import method_decorator

from .forms import SignUpFormWithRusError, AuthFormWithRusError, UserForgotPasswordForm
from django.views.generic.edit import FormView, UpdateView
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from utils.for_account import login_check, check_recaptcha


# Вариант регистрации на базе класса FormView
class RegisterFormView(FormView):
    # Указажем какую форму мы будем использовать для регистрации наших пользователей, в нашем случае
    # это UserCreationForm - стандартный класс Django унаследованный, заменил на SignUpForm из forms
    form_class = SignUpFormWithRusError
    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "/account/login/"
    # Шаблон, который будет использоваться при отображении представления.
    template_name = "register.html"

    def form_valid(self, form):
        if self.request.recaptcha_is_valid:
            form.save()
            """
            send_mail('Django mail', 'This e-mail was sent with Django.',
            'your_account@gmail.com', [form.cleaned_data.get("email")], fail_silently=False)
            """
            return super(RegisterFormView, self).form_valid(form)
            # Функция super( тип [ , объект или тип ] )
            # Возвратите объект прокси, который делегирует вызовы метода родительскому или родственному классу типа .
        return render(self.request, 'register.html', self.get_context_data())

    def form_invalid(self, form):
        return super(RegisterFormView, self).form_invalid(form)


# Функция для установки сессионного ключа.
# По нему django будет определять, выполнил ли вход пользователь.
from django.contrib.auth import login


class LoginFormView(FormView):
    form_class = AuthFormWithRusError
    # Аналогично регистрации, только используем шаблон аутентификации.
    template_name = "login.html"
    # В случае успеха перенаправим на главную.
    success_url = "/"

    def form_valid(self, form):
        # Получаем объект пользователя на основе введённых в форму данных.
        self.user = form.get_user()
        if self.user.is_active:
            # Выполняем аутентификацию пользователя.
            login(self.request, self.user)
        else:
            raise forms.ValidationError("Пароль действителен, но учетная запись была заблокирована!")
            # "The password is valid, but the account has been disabled!")

        return super(LoginFormView, self).form_valid(form)


from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.base import View
from django.contrib.auth import logout


@method_decorator(login_check(), name='dispatch')
class LogoutView(View):
    def get(self, request):
        # Выполняем выход для пользователя, запросившего данное представление.
        logout(request)
        # После чего, перенаправляем пользователя на главную страницу.
        return HttpResponseRedirect("/")


from django.core.mail import BadHeaderError  # send_mail,
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .models import CustomUser


# from utils.for_account import check_recaptcha


# @check_recaptcha
def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = UserForgotPasswordForm(request.POST)
        if password_reset_form.is_valid():
            if request.recaptcha_is_valid:
                username = password_reset_form.cleaned_data['username']
                email = password_reset_form.cleaned_data['email']
                associated_users = CustomUser.objects.filter(Q(email=email, username=username))
                if associated_users.exists():
                    for user in associated_users:
                        subject = "Запрос на сброс пароля"
                        email_template_name = "password_reset_email.txt"
                        c = {
                            "email": user.email,
                            'domain': 'PavelLip.pythonanywhere.com',
                            'site_name': 'Website',
                            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                            "user": user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                        }
                        email = render_to_string(email_template_name, c)
                        try:
                            send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                        except BadHeaderError:
                            return HttpResponse('Invalid header found.')
                        return redirect("password_reset/done/")
    password_reset_form = UserForgotPasswordForm()
    return render(request=request, template_name="password_reset.html", context={"form": password_reset_form})


"""
class UserForgotPasswordFormView(FormView):
    form_class = UserForgotPasswordForm
    template_name = "pasreset.html"
    success_url = "/account/pasreset/message/"
    def form_valid(self, form):

        send_mail('Django pas mail', str(form.email),
            'your_account@gmail.com' , ['lipaikin.pavel@yandex.ru'], fail_silently=False)
        return super(UserForgotPasswordFormView, self).form_valid(form)
"""

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from blog.models import Article


@login_check()
def profile(request, id):
    context = {"self_profile": True, }
    if request.user.id != id:
        user = get_object_or_404(get_user_model(), id=id, is_active=True)
        context["self_profile"] = False
        if request.user in user.followers.all():
            context["is_follower"] = True
        else:
            context["is_follower"] = False
    else:
        user = request.user
    context["user_profile"] = user
    if context["user_profile"].bio is None:
        context["user_profile"].bio = "Пользователь еще не добавил описание"
    context['count_article'] = len(Article.objects.filter(author=user))
    context['count_followers'] = len(user.followers.all())
    context['count_following'] = len(user.following.all())

    return render(request, "profile.html", context)


@method_decorator(login_check(), name='dispatch')
class ProfileFollowingCreateView(View):
    """
    Создание подписки для пользователей
    """
    model = CustomUser

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def post(self, request, id):
        user = get_object_or_404(self.model, id=id)
        if user.followers.contains(request.user):
            user.followers.remove(request.user)
            status = False
        else:
            user.followers.add(request.user)
            status = True
        data = {
            'is_follower': status,
            'count_followers': len(user.followers.all())
        }
        return JsonResponse(data, status=200)


from .forms import CustomUserChangeFormRus
from django.urls import reverse, reverse_lazy


@method_decorator(check_recaptcha, name='dispatch')
@method_decorator(login_check(), name='dispatch')
class UpdateFormView(UpdateView):
    model = CustomUser
    form_class = CustomUserChangeFormRus
    template_name = "update.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        return context

    def form_valid(self, form):
        if self.request.recaptcha_is_valid:
            form.save()
            return super(UpdateFormView, self).form_valid(form)
        return super(UpdateFormView, self).form_invalid(form)

    def form_invalid(self, form):
        return super(UpdateFormView, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'id': self.request.user.id})


def password_reset_request_auth(request):
    email = request.user.email
    username = request.user.username
    associated_users = CustomUser.objects.filter(Q(email=email, username=username))
    if associated_users.exists():
        for user in associated_users:
            subject = "Запрос на сброс пароля"
            email_template_name = "password_reset_email.txt"
            c = {
                "email": user.email,
                'domain': 'PavelLip.pythonanywhere.com',
                'site_name': 'Website',
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
            }
            email = render_to_string(email_template_name, c)
            try:
                # send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                pass
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("password_reset/done/")
    return render(request, "error/500.html", {})


# собственные варианты ошибок
def custom_page_not_found_view(request, exception):
    return render(request, "error/404.html", {})


def custom_error_view(request, exception=None):
    return render(request, "error/500.html", {})


def custom_permission_denied_view(request, exception=None):
    return render(request, "error/403.html", {})


def custom_bad_request_view(request, exception=None):
    return render(request, "error/400.html", {})


def ban(request):
    return render(request, 'error/banip.html', {})
