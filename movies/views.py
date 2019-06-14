from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from .models import (Movie, Genre, Score)


class MovieListView(ListView):
    model = Movie
    paginate_by = 24
    ordering = ['-added_date']

    def get_context_data(self, **kwargs):
        context = super(MovieListView, self).get_context_data()
        context['genre_list'] = Genre.objects.all()
        return context


class MovieDetailView(DetailView):
    model = Movie


class MovieToFavoriteView(View):

    def post(self, request, *args, **kwargs):
        print(request)
        print(args)
        print(kwargs)
        return HttpResponse('Movie ID: {0}'.format(self.kwargs['pk']))


class MovieByGenreListView(ListView):
    model = Movie
    paginate_by = 24
    template_name = 'movies/movie_by_genre.html'

    def get_queryset(self):
        genre = get_object_or_404(Genre, title=self.kwargs['genre'])
        return Movie.objects.filter(genre=genre)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MovieByGenreListView, self).get_context_data()
        context['genre_list'] = Genre.objects.all()
        context['genre'] = get_object_or_404(Genre, title=self.kwargs['genre'])
        return context


class ScoreListView(ListView):
    model = Score
    paginate_by = 24
    ordering = ['-date']
