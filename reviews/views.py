from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import ReviewForm
from .models import Review


def reviews_home(request):
    reviews = Review.objects.all().order_by('-date_posted')
    review_average = Review.get_average_ratings
    return render(request, 'reviews/reviews_home.html', {'reviews': reviews, 'review_average': review_average})


def specific_review(request, pk):
    review = get_object_or_404(Review, id=pk)
    return render(request, 'reviews/specific_review.html', {'review': review})


def write_review(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            review_form = ReviewForm(request.POST or None)
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
    review_to_edit = get_object_or_404(Review, id=pk)

    # users can only edit their own reviews
    if review_to_edit.poster != request.user:
        messages.error(request, "You cannot edit this review")
        return redirect('reviews-home')

    if request.method == 'POST':
        edit_review_form = ReviewForm(request.POST, instance=review_to_edit)
        if edit_review_form.is_valid():
            review_to_edit.save()
            messages.success(request, "Your review has been edited")
            return redirect('reviews-home')
        else:
            messages.error(request, "There was an error with your submission")
    else:
        # pre-populate review form with existing object data (previously entered data) upon GET request
        edit_review_form = ReviewForm(instance=review_to_edit)

    return render(request, 'reviews/edit_review.html', {'review_to_edit': review_to_edit, 'edit_review_form': edit_review_form})


def delete_review(request, pk):
    review_to_delete = get_object_or_404(Review, id=pk)

    # users can only delete their own reviews
    if review_to_delete.poster != request.user:
        messages.error(request, "You cannot delete this review")
        return redirect('reviews-home')

    return render(request, 'reviews/confirm_delete.html', {'review_to_delete': review_to_delete})


def confirm_delete_review(request, pk):
    review_to_delete = get_object_or_404(Review, id=pk)

    # users can only delete their own reviews
    if review_to_delete.poster != request.user:
        messages.error(request, "You cannot delete this review")
        return redirect('reviews-home')

    review_to_delete.delete()

    return redirect('reviews-home')
