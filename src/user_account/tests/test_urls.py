from django.core.management import call_command
from django.urls import reverse
from django.test import TestCase
from django.test import Client


class UrlsAvailabilityTests(TestCase):

    def setUp(self):
        call_command('loaddata', 'tests/fixtures/user_accounts.json', verbosity=0)

        self.client = Client()

    def test_public_url(self):

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
            reverse('account:profile'),
            reverse('account:logout'),

        ]
        for url in private_urls:
            response = self.client.get(url)
            self.assertRedirects(response, '{}?next={}'.format(reverse('account:login'), url))

    def test_auth_user_urls(self):

        self.client.login(username='anna123', password='nikita160295Angel')

        private_urls = [
            (reverse('account:profile'), 'Edit current user profile'),
            (reverse('account:logout'), 'Logout'),

        ]
        for url, content in private_urls:
            response = self.client.get(url)
            assert response.status_code == 200
            assert content in response.content.decode()
