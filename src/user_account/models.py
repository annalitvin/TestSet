import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Count, Sum


class User(AbstractUser):
    image = models.ImageField(default='default.jpg', upload_to='pics')
    avr_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    number_tests_passed = models.PositiveIntegerField(null=True, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True, default=datetime.date.today)

    def update_score(self):
        self.avr_score = self.test_results.aggregate(points=Sum('avr_score')).get('points', 0.0) / \
                         self.test_results.count()
