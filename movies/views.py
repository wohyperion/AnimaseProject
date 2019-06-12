from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from .models import (Movie, Genre)


# Create your views here.
def index(request):
    context = {}
    return render(request, 'base.html', context)


class MovieListView(ListView):
    model = Movie
    paginate_by = 24

    def get_context_data(self, **kwargs):
        context = super(MovieListView, self).get_context_data()
        context['genre_list'] = Genre.objects.all()
        return context


class GenreMovieListView(ListView):
    model = Movie
    paginate_by = 24
    template_name = 'movies/movie_by_genre.html'

    def get_queryset(self):
        genre = get_object_or_404(Genre, title=self.kwargs['genre'])
        return Movie.objects.filter(genre=genre)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GenreMovieListView, self).get_context_data()
        context['genre_list'] = Genre.objects.all()
        context['genre'] = get_object_or_404(Genre, title=self.kwargs['genre'])
        return context


class MovieDetailView(DetailView):
    model = Movie
