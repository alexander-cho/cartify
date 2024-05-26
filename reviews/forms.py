from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    text_content = forms.CharField(label='',
                                   widget=forms.Textarea(attrs={
                                       'placeholder': 'Enter your review here',
                                       'class': 'form-control'}),
                                   required=True)
    star_rating = forms.IntegerField(label='',
                                     widget=forms.NumberInput(attrs={
                                         'placeholder': 'Rate from 1 to 5',
                                         'class': 'form-control'}),
                                     required=True)

    class Meta:
        model = Review
        fields = ['text_content', 'star_rating']
