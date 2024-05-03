from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class Review(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    text_content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    star_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    @staticmethod
    def get_average_ratings():
        average_rating = Review.objects.aggregate(Avg('star_rating'))['star_rating__avg']
        if average_rating is None:
            return 0  # if there are no reviews yet
        else:
            return average_rating

    def __str__(self):
        return f'{self.poster} - {self.star_rating} on {self.date_posted}'
