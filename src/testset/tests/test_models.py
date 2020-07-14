import datetime

from django.core.management import call_command
from django.test import TestCase

from testset.models import Test, Question


class TestModelTest(TestCase):

    def setUp(self):
        call_command('loaddata', 'tests/fixtures/user_accounts.json', verbosity=0)
        call_command('loaddata', 'tests/fixtures/tests.json', verbosity=0)

    def tearDown(self):
        pass

    def test_question_count(self):
        test = Test.objects.first()
        self.assertEqual(test.questions_count(), 3)

    def test_last_run(self):
        test = Test.objects.first()
        dt = datetime.datetime.strptime('2020-07-04T15:27:50.406Z', "%Y-%m-%dT%H:%M:%S.%f%z")

        self.assertEqual(test.last_run(), dt)
