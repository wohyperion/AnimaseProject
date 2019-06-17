from django.forms import ModelForm

from .models import Movie


class MovieForm(ModelForm):

    class Meta:
        model = Movie
        exclude = ['user', 'added_date', 'allowed']
