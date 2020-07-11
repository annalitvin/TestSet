from django.core.management import call_command
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from testset.models import Test

PK = 1


class BaseFlowTest(TestCase):

    def setUp(self):
        call_command('loaddata', 'tests/fixtures/user_accounts.json', verbosity=0)
        call_command('loaddata', 'tests/fixtures/tests.json', verbosity=0)
        self.client = Client()
        self.client.login(username='anna123', password='nikita160295Angel')

    def test_basic_flow(self):
        response = self.client.get(reverse('testset:start', kwargs={'test_pk': PK}))
        assert response.status_code == 200
        assert 'START ▶️' in response.content.decode()

        test = Test.objects.get(pk=PK)
        questions_count = test.questions_count()
        url = reverse('testset:next', kwargs={'pk': PK})

        for step in range(1, questions_count+1):
            response = self.client.get(url)
            assert response.status_code == 200
            assert 'Submit' in response.content.decode()
            response = self.client.post(
                path=url,
                data={
                    'answer_1': "1"
                }
            )
            if step < questions_count:
                self.assertRedirects(response, url)
            else:
                assert response.status_code == 200

        assert 'START ANOTHER TEST ▶️' in response.content.decode()

    def test_success_passed(self):
        response = self.client.get(reverse('testset:start', kwargs={'test_pk': PK}))
        assert response.status_code == 200
        assert 'START ▶️' in response.content.decode()

        test = Test.objects.get(pk=PK)
        questions_count = test.questions_count()
        url = reverse('testset:next', kwargs={'pk': PK})

        answers = [
            {
                'answer_3': "1",
                'answer_4': "1"
            },
            {
                'answer_3': "1",
            },
            {
                'answer_2': "1",
            },
        ]

        for step, answer in enumerate(answers, 1):
            response = self.client.get(url)
            assert response.status_code == 200
            assert 'Submit' in response.content.decode()

            response = self.client.post(
                path=url,
                data=answer
            )

            if step < questions_count:
                self.assertRedirects(response, url)
            else:
                assert response.status_code == 200

        self.assertIn('START ANOTHER TEST ▶', response.content.decode())
        self.assertIn('3 of 3 (100.00%)', response.content.decode())
        self.assertIn('3.0', response.content.decode())

    def test_success_failed(self):
        response = self.client.get(reverse('testset:start', kwargs={'test_pk': PK}))
        assert response.status_code == 200
        assert 'START ▶️' in response.content.decode()

        test = Test.objects.get(pk=PK)
        questions_count = test.questions_count()
        url = reverse('testset:next', kwargs={'pk': PK})

        answers = [
            {
                'answer_3': "1",
                'answer_4': "1"
            },
            {
                'answer_1': "1",
            },
            {
                'answer_1': "1",
            },
        ]

        for step, answer in enumerate(answers, 1):
            response = self.client.get(url)
            assert response.status_code == 200
            assert 'Submit' in response.content.decode()

            response = self.client.post(
                path=url,
                data=answer
            )

            if step < questions_count:
                self.assertRedirects(response, url)
            else:
                assert response.status_code == 200

        self.assertIn('START ANOTHER TEST ▶', response.content.decode())
        self.assertIn('1 of 3 (33.33%)', response.content.decode())
        self.assertIn('1.83', response.content.decode())

    def test_answers_exists(self):
        response = self.client.get(reverse('testset:start', kwargs={'test_pk': PK}))
        assert response.status_code == 200
        assert 'START ▶️' in response.content.decode()

        test = Test.objects.get(pk=PK)
        questions_count = test.questions_count()
        url = reverse('testset:next', kwargs={'pk': PK})

        answers = [
            {
                'answer_3': "1",
                'answer_4': "1"
            },
            {

            },
            {
                'answer_1': "1",
            },
        ]

        for step, answer in enumerate(answers, 1):
            response = self.client.get(url)
            assert response.status_code == 200
            assert 'Submit' in response.content.decode()

            response = self.client.post(
                path=url,
                data=answer
            )

            if step < questions_count:
                if not answer:
                    response = self.client.get(reverse('testset:next', kwargs={'pk': PK}))
                    self.assertIn('ERROR: You should select at least 1 answer!', response.content.decode())
