from django.shortcuts import render


def review_home(request):
    return render(request, 'reviews/review_home.html')


def specific_review(request):
    return render(request, 'reviews/specific_review.html')


def write_review(request):
    return render(request, 'reviews/write_review.html')
