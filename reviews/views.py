from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import ReviewForm
from .models import Review


def review_home(request):
    reviews = Review.objects.all().order_by('-date_posted')
    return render(request, 'reviews/review_home.html', {'reviews': reviews})


def specific_review(request, pk):
    review = get_object_or_404(Review, id=pk)
    return render(request, 'reviews/specific_review.html', {'review': review})


def write_review(request):
    if request.user.is_authenticated:
        review_form = ReviewForm(request.POST or None)
        if request.method == 'POST':
            if review_form.is_valid():
                # create a review instance without saving it
                review = review_form.save(commit=False)
                # get the user that the review is going to be associated with (poster from model attribute)
                review.poster = request.user
                review.save()
                messages.success(request, "Your review has been saved")
                return redirect('reviews-home')
            else:
                messages.error(request, "There was an error with your submission")
        else:
            review_form = ReviewForm()
            return render(request, 'reviews/write_review.html', {'review_form': review_form})
    else:
        messages.success(request, "You have to be logged in to leave a review")
        return redirect('reviews-home')


def edit_review(request, pk):
    # if a certain amount of time has not passed yet
    pass
