import datetime

from django.contrib import messages
from django.db.models import Max, Count
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.base import View

from testset.models import Test, TestResult, Question, Variant, TestResultDetail
from user_account.models import User


class TestListView(ListView):
    model = Test
    template_name = 'testset/test_list.html'
    context_object_name = 'test_list'

    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset().order_by('-id')
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'Test suites'
        return context


class UserLeaderBoardListView(ListView):
    model = User
    template_name = 'testset/result_list.html'
    context_object_name = 'user_list'

    paginate_by = 5

    # def get_queryset(self):
    #     qs = super().get_queryset().order_by('-avr_score')
    #     qs.select_related('user')
    #     return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'LeaderBoard'
        return context


class TestRunView(View):

    PREFIX = 'answer_'
    variants_count = []

    def get(self, request, pk, seq_nr):
        print(self.variants_count)

        question = Question.objects.filter(test__id=pk, number=seq_nr).first()

        variants = [
            variant.text
            for variant in question.variants.all()
        ]
        return render(request, 'testset/test_run.html', {'question': question,
                                                         'answers': variants,
                                                         'prefix': self.PREFIX})

    def post(self, request, pk, seq_nr):

        test = Test.objects.get(pk=pk)
        question = Question.objects.filter(test__id=pk, number=seq_nr).first()

        variants = Variant.objects.filter(
            question=question
        ).all()

        choices = {
            k.replace(self.PREFIX, ''): True
            for k in request.POST if k.startswith(self.PREFIX)
        }
        self.variants_count.append(variants.count())

        if not choices:
            messages.error(self.request, extra_tags='danger', message="ERROR: You should select at least 1 answer!")
            return redirect(reverse('testset:run_step', kwargs={'pk': pk, 'seq_nr': seq_nr}))

        current_test_result = TestResult.objects.filter(
            test=test,
            user=request.user,
            is_completed=False).last()

        for idx, variant in enumerate(variants, 1):
            value = choices.get(str(idx), False)
            TestResultDetail.objects.create(
                test_result=current_test_result,
                question=question,
                variant=variant,
                is_correct=(value == variant.is_correct)
            )

        if question.number < test.questions_count():
            return redirect(reverse('testset:run_step', kwargs={'pk': pk, 'seq_nr': seq_nr + 1}))
        else:
            qs = current_test_result.test_result_details.values('question').filter(is_correct=True).\
                annotate(Count('is_correct'))

            is_correct = 0
            for qs_item in zip(qs, self.variants_count):
                if qs_item[0].get('is_correct__count') == qs_item[1]:
                    is_correct += 1

            self.variants_count.clear()

            current_test_result.finish()
            current_test_result.save()
            current_user = User.objects.get(pk=request.user.pk)
            current_user.update_score()
            current_user.save()

            return render(
                request=request,
                template_name='testset/test_end.html',
                context={
                    'test_result': current_test_result,
                    'time_spent': datetime.datetime.utcnow() - current_test_result.datetime_run.replace(tzinfo=None),
                    'is_correct': is_correct,
                    'questions_count': test.questions_count(),
                    'test': test
                }
            )


class TestStartView(View):

    def get(self, request, test_pk):

        test = Test.objects.get(pk=test_pk)
        test_result = TestResult.objects.create(user=request.user,
                                                test=test)

        best_result = User.objects.aggregate(Max('avr_score')).get('avr_score__max')
        best_result_users = User.objects.filter(avr_score=best_result)

        return render(request, 'testset/test_start.html', {'test': test,
                                                           'test_result': test_result,
                                                           'best_result': best_result,
                                                           'best_result_users': best_result_users})
