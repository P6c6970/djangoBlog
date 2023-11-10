from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

tolerance_levels = {"admin": 0, "moderator": 1, "user": 2}


def get_lvl_permission_name(name):
    lvl = 3
    if name in tolerance_levels:
        lvl = tolerance_levels[name]
    return lvl


def get_lvl_permission(user):
    if user.is_superuser:
        return tolerance_levels["admin"]
    elif user.groups.filter(name='moderator').exists():
        return tolerance_levels["moderator"]
    return tolerance_levels["user"]


def login_check(decorator_arg1="user"):
    lvl = get_lvl_permission_name(decorator_arg1)

    def my_decorator(func):
        def wrapper(arg1, *args, **kwargs):
            if arg1.user.is_authenticated and lvl >= get_lvl_permission(arg1.user):
                return func(arg1, *args, **kwargs)
            return render(arg1, 'error/403.html')

        return wrapper

    return my_decorator


def redirect_authenticated():
    def my_decorator(func):
        def wrapper(arg1, *args, **kwargs):
            if not arg1.user.is_authenticated:
                return func(arg1, *args, **kwargs)

            return HttpResponseRedirect(reverse('profile', args=(arg1.user.id,)))
        return wrapper

    return my_decorator


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


from django.conf import settings
from django.contrib import messages
import requests


def check_recaptcha(function):
    def wrap(request, *args, **kwargs):
        request.recaptcha_is_valid = None
        if request.method == 'POST':
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            if result['success']:
                request.recaptcha_is_valid = True
            else:
                request.recaptcha_is_valid = False
                messages.error(request, 'Invalid reCAPTCHA. Пожалуйста, попробуйте еще раз.')
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
