from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from testset.models import TestResult
from user_account.models import User


@receiver(pre_save, sender=User)
def save_profile(sender, instance, **kwargs):
    count_passed_test = instance.count_passed_tests()
    test_results = instance.test_results.filter(is_completed=True)

    if count_passed_test != 0:
        percent_success_passed = round((sum([test_result.correct_answers_count() for test_result in test_results]) / \
                                        sum([test_result.test_question_count() for test_result in test_results]))
                                       * 100, 2)
        instance.percent_success = percent_success_passed
