from django.core.management import call_command
from django.db.models import Count, Sum
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from testset.models import Test, TestResult, TestResultDetail
from user_account.models import User

PK = 1


class BaseFlowTest(TestCase):
    USERNAME = 'anna123'
    PASSWORD = 'nikita160295Angel'

    def setUp(self):
        call_command('loaddata', 'tests/fixtures/user_accounts.json', verbosity=0)
        call_command('loaddata', 'tests/fixtures/tests.json', verbosity=0)
        self.client = Client()
        self.client.login(username=self.USERNAME, password=self.PASSWORD)

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
        self.client.get(reverse('testset:start', kwargs={'test_pk': PK}))

        test = Test.objects.get(pk=PK)
        questions = test.questions.all()
        url = reverse('testset:next', kwargs={'pk': PK})

        for idx, question in enumerate(questions, 1):
            self.client.get(url)
            correct_answers = {
                f'answer_{idx}': '1'
                for idx, variant in enumerate(question.variants.all(), 1)
                if variant.is_correct
            }
            self.client.post(
                path=url,
                data=correct_answers
            )

        test_result = TestResult.objects.order_by('-id').first()
        self.assertEqual(test.questions_count(), int(test_result.avr_score))

    def test_success_failed(self):
        self.client.get(reverse('testset:start', kwargs={'test_pk': PK}))

        test = Test.objects.get(pk=PK)
        questions = test.questions.all()
        url = reverse('testset:next', kwargs={'pk': PK})

        for idx, question in enumerate(questions, 1):
            self.client.get(url)

            variants = question.variants.all()
            if idx == 2:
                answers = {
                    f'answer_{idx}': '0'
                    for idx, variant in enumerate(variants, 1)
                    if not variant.is_correct
                }
            else:
                answers = {
                    f'answer_{idx}': '1'
                    for idx, variant in enumerate(variants, 1)
                    if variant.is_correct
                }
            self.client.post(
                path=url,
                data=answers
            )

        test_result = TestResult.objects.order_by('-id').first()
        self.assertNotEqual(test.questions_count(), int(test_result.avr_score))

    def test_answers_exists(self):
        self.client.get(reverse('testset:start', kwargs={'test_pk': PK}))

        test = Test.objects.get(pk=PK)
        questions_count = test.questions_count()
        url = reverse('testset:next', kwargs={'pk': PK})

        for num_question, question in enumerate(test.questions.all(), 1):
            self.client.get(url)

            if num_question != 2:
                correct_answers = {
                    f'answer_{idx}': '1'
                    for idx, variant in enumerate(question.variants.all(), 1)
                    if variant.is_correct
                }
            else:
                correct_answers = {}

            self.client.post(
                path=url,
                data=correct_answers
            )

            if num_question < questions_count:
                if not correct_answers:
                    response = self.client.get(reverse('testset:next', kwargs={'pk': PK}))
                    self.assertIn('ERROR: You should select at least 1 answer!', response.content.decode())
