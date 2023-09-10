from .models import BanIp
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from utils.for_account import get_client_ip


def check_ip(get_response):
    def middleware(request):
        # забираем IP адрес из запроса
        ip = get_client_ip(request)
        # получаем или создаём новую запись об IP, с которого вводится пароль, на предмет блокировки
        try:
            obj = BanIp.objects.get(ip_address=ip)
            # если IP заблокирован и время разблокировки не настало
            if obj.status is True and obj.time_unblock > timezone.now():
                path = request.path_info
                if path != reverse('ban'):
                    return HttpResponseRedirect(reverse('ban'))
            elif obj.status is True and obj.time_unblock < timezone.now():
                obj.delete()
        except BanIp.DoesNotExist:
            pass

        response = get_response(request)
        return response

    return middleware
