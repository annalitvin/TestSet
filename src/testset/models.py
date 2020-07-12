from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Count, Sum


class Topic(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return f'{self.title}'


class Test(models.Model):
    LEVEL_CHOICES = (
        (1, 'Basic'),
        (2, 'Middle'),
        (3, 'Advanced'),
    )
    MIN_LIMIT = 3
    MAX_LIMIT = 20

    topic = models.ForeignKey(to=Topic, related_name='tests', null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, null=True, blank=True)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=2)
    image = models.ImageField(default='default.png', upload_to='covers')

    def __str__(self):
        return f'{self.title}'

    def questions_count(self):
        return self.questions.count()

    def last_run(self):
        last_run = self.test_results.order_by('-datetime_run').first()
        if last_run:
            return last_run.datetime_run
        return ''

    def number_runs(self):
        return self.test_results.count()


class Question(models.Model):
    MIN_LIMIT = 3
    MAX_LIMIT = 6

    test = models.ForeignKey(to=Test, related_name='questions', on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(MAX_LIMIT)],
                                              default=1)
    text = models.CharField(max_length=64)
    description = models.TextField(max_length=512, null=True, blank=True)

    def __str__(self):
        return f'{self.text}'

    def next(self):
        return 'next'

    def prev(self):
        return 'prev'


class Variant(models.Model):
    text = models.CharField(max_length=64)
    question = models.ForeignKey(to=Question, related_name='variants', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text} -- {self.is_correct}'


class TestResult(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='test_results', on_delete=models.CASCADE)
    test = models.ForeignKey(to=Test, related_name='test_results', on_delete=models.CASCADE)

    datetime_run = models.DateTimeField(auto_now_add=True, null=True)
    is_completed = models.BooleanField(default=False, null=True)
    is_new = models.BooleanField(default=True)

    avr_score = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                    validators=[MinValueValidator(0), MaxValueValidator(100)], null=True)

    def update_score(self):
        qs = self.test_result_details.values('question').annotate(
            num_answers=Count('question'),
            score=Sum('is_correct')
        )
        self.avr_score = sum(
            int(entry['score']) / entry['num_answers']
            for entry in qs
        )

    def correct_answers_count(self):
        qs = self.test_result_details.values('question').annotate(
            num_answers=Count('question'),
            points=Sum('is_correct')
        )
        return sum(e['num_answers'] == int(e['points']) for e in qs)

    def score_info(self):
        num_questions = self.test.questions_count()
        num_answers = self.correct_answers_count()
        return f'{num_answers} of {num_questions} ({(num_answers / num_questions) * 100:.2f}%)'

    def percent_correct_answers(self):
        num_questions = self.test.questions_count()
        num_answers = self.correct_answers_count()
        return num_answers / num_questions

    def test_question_count(self):
        num_questions = self.test.questions_count()
        return num_questions

    def finish(self):
        self.update_score()
        self.is_completed = True


class TestResultDetail(models.Model):
    test_result = models.ForeignKey(to=TestResult, related_name='test_result_details', on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, on_delete=models.CASCADE)
    variant = models.ForeignKey(to=Variant, related_name='test_result_details', on_delete=models.CASCADE)
    is_correct = models.BooleanField(null=True, default=False)
