import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
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


class UserLeaderBoardListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'testset/result_list.html'
    context_object_name = 'user_list'
    login_url = reverse_lazy('account:login')

    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().order_by('-avr_score')
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'LeaderBoard'
        return context


class TestRunView(LoginRequiredMixin, View):
    login_url = reverse_lazy('account:login')

    PREFIX = 'answer_'
    variants_count = []

    def get(self, request, pk):

        if 'testresult' not in request.session:
            return HttpResponse('ERROR!')

        testresult_step = request.session.get('testresult_step', 1)
        request.session['testresult_step'] = testresult_step

        question = Question.objects.get(test__id=pk, number=testresult_step)

        variants = [
            variant.text
            for variant in question.variants.all()
        ]
        return render(request, 'testset/test_run.html', {'question': question,
                                                         'answers': variants,
                                                         'prefix': self.PREFIX,
                                                         })

    def post(self, request, pk):

        if 'testresult_step' not in request.session:
            return HttpResponse('ERROR!')

        testresult_step = request.session['testresult_step']

        test = Test.objects.get(pk=pk)
        question = Question.objects.get(test__id=pk, number=testresult_step)

        variants = Variant.objects.filter(
            question=question
        ).all()

        questions_count = test.questions_count()

        choices = {
            k.replace(self.PREFIX, ''): True
            for k in request.POST if k.startswith(self.PREFIX)
        }
        self.variants_count.append(variants.count())

        if not choices:
            messages.error(self.request, extra_tags='danger', message="ERROR: You should select at least 1 answer!")
            return redirect(reverse('testset:next', kwargs={'pk': pk}))

        if len(choices) == len(variants):
            messages.error(self.request, extra_tags='danger', message="ERROR: You can't select ALL answer!")
            return redirect(reverse('testset:next', kwargs={'pk': pk}))

        current_test_result = TestResult.objects.get(
            id=request.session['testresult']
        )

        for idx, variant in enumerate(variants, 1):
            value = choices.get(str(idx), False)
            TestResultDetail.objects.create(
                test_result=current_test_result,
                question=question,
                variant=variant,
                is_correct=(value == variant.is_correct)
            )

        if question.number < questions_count:
            current_test_result.is_new = False
            current_test_result.save()
            request.session['testresult_step'] = testresult_step + 1
            return redirect(reverse('testset:next', kwargs={'pk': pk}))
        else:
            del request.session['testresult']
            del request.session['testresult_step']

            current_test_result.finish()
            current_test_result.save()

            score_info = current_test_result.score_info()
            score_result = current_test_result.avr_score

            return render(
                request=request,
                template_name='testset/test_end.html',
                context={
                    'test_result': current_test_result,
                    'score_result': round(score_result, 2),
                    'time_spent': datetime.datetime.utcnow() - current_test_result.datetime_run.replace(tzinfo=None),
                    'score_info': score_info,
                    'test': test
                }
            )


class TestStartView(LoginRequiredMixin, View):
    login_url = reverse_lazy('account:login')

    def get(self, request, test_pk):

        test = Test.objects.get(pk=test_pk)

        test_result_id = request.session.get('testresult')

        if test_result_id:
            test_result = TestResult.objects.get(id=test_result_id)
        else:
            test_result = TestResult.objects.create(
                user=request.user,
                test=test
            )

        request.session['testresult'] = test_result.id

        best_result = User.objects.aggregate(Max('avr_score')).get('avr_score__max')
        best_result_users = User.objects.filter(avr_score=best_result)

        return render(request, 'testset/test_start.html', {'test': test,
                                                           'test_result': test_result,
                                                           'best_result': round(best_result, 2),
                                                           'best_result_users': best_result_users,
                                                           })
