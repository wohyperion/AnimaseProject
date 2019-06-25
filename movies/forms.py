from django import forms

from .models import Movie, Score


class MovieForm(forms.ModelForm):

    class Meta:
        model = Movie
        exclude = ['user', 'added_date', 'allowed']


class ScoreForm(forms.ModelForm):

    class Meta:
        model = Score
        fields = ['message', 'value']
