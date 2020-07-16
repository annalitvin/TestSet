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
        response = self.client.get(reverse('testset:start', kwargs={'test_pk': PK}))
        assert response.status_code == 200
        assert 'START ▶️' in response.content.decode()

        test = Test.objects.get(pk=PK)
        questions_count = test.questions_count()
        user = User.objects.get(username=self.USERNAME)
        url = reverse('testset:next', kwargs={'pk': PK})

        test_result = TestResult.objects.create(
            user=user,
            test=test
        )

        current_test_result = TestResult.objects.get(
            id=test_result.id
        )

        answers = []

        for question in test.questions.all():
            answer = {}
            for n, variant in enumerate(question.variants.all(), 1):
                if variant.is_correct:
                    answer[f'answer_{n}'] = "1"

                TestResultDetail.objects.create(
                    test_result=current_test_result,
                    question=question,
                    variant=variant,
                    is_correct=True
                )

            answers.append(answer)

        test_result = test.test_results.last()

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
                test_result.finish()
                test_result.save()
                assert response.status_code == 200

        self.assertIn('START ANOTHER TEST ▶', response.content.decode())
        self.assertIn(test_result.score_info(), response.content.decode())
        self.assertIn(test_result.get_avr_score, response.content.decode())

    def test_success_failed(self):
        response = self.client.get(reverse('testset:start', kwargs={'test_pk': PK}))
        assert response.status_code == 200
        assert 'START ▶️' in response.content.decode()

        test = Test.objects.get(pk=PK)
        questions_count = test.questions_count()
        user = User.objects.get(username=self.USERNAME)
        url = reverse('testset:next', kwargs={'pk': PK})

        test_result = TestResult.objects.create(
            user=user,
            test=test
        )

        current_test_result = TestResult.objects.get(
            id=test_result.id
        )

        answers = []

        for num_question, question in enumerate(test.questions.all(), 1):
            answer = {}
            is_correct = True
            for n, variant in enumerate(question.variants.all(), 1):
                if num_question == 1:
                    if not variant.is_correct:
                        is_correct = False
                        answer[f'answer_{n}'] = "0"
                else:
                    if variant.is_correct:
                        answer[f'answer_{n}'] = "1"

                TestResultDetail.objects.create(
                    test_result=current_test_result,
                    question=question,
                    variant=variant,
                    is_correct=is_correct
                )

            answers.append(answer)

        test_result = test.test_results.last()

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
                test_result.finish()
                test_result.save()
                assert response.status_code == 200

        self.assertIn('START ANOTHER TEST ▶', response.content.decode())
        self.assertIn(test_result.score_info(), response.content.decode())
        self.assertIn(test_result.get_avr_score, response.content.decode())

    def test_answers_exists(self):
        response = self.client.get(reverse('testset:start', kwargs={'test_pk': PK}))
        assert response.status_code == 200
        assert 'START ▶️' in response.content.decode()

        test = Test.objects.get(pk=PK)
        questions_count = test.questions_count()
        url = reverse('testset:next', kwargs={'pk': PK})

        answers = []

        for num_question, question in enumerate(test.questions.all(), 1):
            answer = {}
            for n, variant in enumerate(question.variants.all(), 1):
                if num_question == 2:
                    continue
                if variant.is_correct:
                    answer[f'answer_{n}'] = "1"

            answers.append(answer)

        for step, answer in enumerate(answers, 1):
            response = self.client.get(url)
            assert response.status_code == 200
            assert 'Submit' in response.content.decode()

            self.client.post(
                path=url,
                data=answer
            )

            if step < questions_count:
                if not answer:
                    response = self.client.get(reverse('testset:next', kwargs={'pk': PK}))
                    self.assertIn('ERROR: You should select at least 1 answer!', response.content.decode())
