from django.test import RequestFactory, TestCase
from django.utils import timezone
from django.urls import reverse

from account.middleware import check_ip
from account.models import BanIp
from datetime import timedelta


class CheckIpMiddlewareTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_ip_blocked_redirects_to_ban_page(self):
        """Tests that if the IP is blocked, the middleware redirects to the 'ban' page."""
        ip = '127.0.0.1'
        BanIp.objects.create(ip_address=ip, status=True, time_unblock=timezone.now() + timedelta(days=1))

        request = self.factory.get('/')
        request.META['REMOTE_ADDR'] = ip

        middleware = check_ip(lambda request: None)
        response = middleware(request)

        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(response.url, reverse('ban'))

    def test_ip_unblocked_passes_through(self):
        """Tests that if the IP is not blocked, the middleware does not modify the response."""
        ip = '127.0.0.1'
        BanIp.objects.create(ip_address=ip, status=False, time_unblock=timezone.now())

        request = self.factory.get('/')
        request.META['REMOTE_ADDR'] = ip

        middleware = check_ip(lambda request: None)
        response = middleware(request)

        self.assertIsNone(response)  # The response should not be modified

    def test_nonexistent_ip_passes_through(self):
        """Tests that if the IP is not in the database, the middleware does not modify the response."""
        ip = '127.0.0.1'

        request = self.factory.get('/')
        request.META['REMOTE_ADDR'] = ip

        middleware = check_ip(lambda request: None)
        response = middleware(request)

        self.assertIsNone(response)  # The response should not be modified

    def test_expired_ip_unblock_deletes_entry(self):
        """Tests that if the IP is blocked but the unblock time has passed, the middleware deletes the entry from the database."""
        ip = '127.0.0.1'
        BanIp.objects.create(ip_address=ip, status=True, time_unblock=timezone.now() - timedelta(days=1))

        request = self.factory.get('/')
        request.META['REMOTE_ADDR'] = ip

        middleware = check_ip(lambda request: None)
        response = middleware(request)

        self.assertIsNone(response)  # The response should not be modified
        self.assertEqual(BanIp.objects.filter(ip_address=ip).count(), 0)
