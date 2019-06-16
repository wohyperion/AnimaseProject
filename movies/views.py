from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.http import HttpResponse, HttpResponseForbidden

from .models import (Movie, Genre, Score, Favorite)


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

    def get_context_data(self, **kwargs):
        context = super(MovieDetailView, self).get_context_data()

        try:
            favorite = Favorite.objects.get(movie_id=self.kwargs['pk'], user_id=self.request.user.pk)
        except Favorite.DoesNotExist:
            favorite = None

        context['favorite'] = favorite
        return context


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


class FavoriteMovieView(View):
    http_method_names = ['post', 'delete']

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        if get_object_or_404(Movie, pk=self.kwargs['pk']):
            obj, created = Favorite.objects.get_or_create(
                movie_id=self.kwargs['pk'],
                user_id=request.user.pk
            )

            if not created:
                obj.delete()

            return HttpResponse(created)
