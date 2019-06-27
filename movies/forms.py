from django import forms
from django.contrib.auth.models import User

from .models import Movie, Score


class MovieForm(forms.ModelForm):

    class Meta:
        model = Movie
        exclude = ['user', 'added_date', 'allowed']


class ScoreForm(forms.ModelForm):

    class Meta:
        model = Score
        fields = ['message', 'value']


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
