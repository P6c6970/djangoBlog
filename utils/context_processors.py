from django.conf import settings


def recaptcha_public_key(request):
    return {'RECAPTCHA_PUBLIC_KEY': settings.RECAPTCHA_PUBLIC_KEY}
