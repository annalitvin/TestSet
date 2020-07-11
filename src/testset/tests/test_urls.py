from django.urls import reverse
from django.test import TestCase
from django.test import Client


class UrlsAvailabilityTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_public_url(self):
        urls = [
            (reverse('index'), 'Welcome to TestSet!'),
            (reverse('testset:list'), 'Test suites'),
        ]
        for url, content in urls:
            response = self.client.get(url)
            assert response.status_code == 200
            assert content in response.content.decode()

    def test_private_urls(self):
        private_urls = [
            reverse('testset:leader_bord'),
        ]
        for url in private_urls:
            response = self.client.get(url)
            self.assertRedirects(response, '{}?next={}'.format(reverse('account:login'), url))
