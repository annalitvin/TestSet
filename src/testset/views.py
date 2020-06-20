from django.views.generic import ListView

from testset.models import Test, TestResult


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
    model = TestResult
    template_name = 'testset/result_list.html'
    context_object_name = 'result_list'

    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset().order_by('-avg_score')
        qs.select_related('user')
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'LeaderBoard'
        return context
