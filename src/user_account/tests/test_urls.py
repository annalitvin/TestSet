from django.urls import reverse
from django.test import TestCase
from django.test import Client


class UrlsAvailabilityTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.client.login(username='anna123', password='nikita160295Angel')

    def test_public_url(self):

        self.client.logout()
        urls = [
            (reverse('account:registration'), 'Register new user'),
            (reverse('account:login'), 'Login as a user'),
        ]
        for url, content in urls:
            response = self.client.get(url)
            assert response.status_code == 200
            assert content in response.content.decode()

    def test_private_urls(self):

        private_urls = [
            (reverse('account:profile'), 'Edit current user profile'),
            (reverse('account:logout'), 'Logout'),

        ]
        for url, content in private_urls:
            response = self.client.get(url)
            self.assertRedirects(response, '{}?next={}'.format(reverse('account:login'), url))
