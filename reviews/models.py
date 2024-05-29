from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg


class Review(models.Model):
    poster = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    text_content = models.TextField(max_length=500)
    date_posted = models.DateTimeField(auto_now_add=True)
    star_rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    @staticmethod
    def get_average_ratings():
        average_rating = Review.objects.aggregate(Avg('star_rating'))['star_rating__avg']
        rounded_rating = round(average_rating, 2)
        if average_rating is None:
            # if there are no reviews yet
            return 0
        else:
            return rounded_rating

    def __str__(self):
        return f'{self.poster} - {self.star_rating} on {self.date_posted}'
