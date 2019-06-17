from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.serializers import serialize

from .models import (Movie, Genre, Score, Favorite, Studio)
from .forms import (MovieForm)


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
    ordering = ['-added_date']

    def get_queryset(self):
        genre = get_object_or_404(Genre, title=self.kwargs['genre'])
        return Movie.objects.filter(genre=genre)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MovieByGenreListView, self).get_context_data()
        context['genre_list'] = Genre.objects.all()
        context['genre'] = get_object_or_404(Genre, title=self.kwargs['genre'])
        return context


class MovieCreateView(LoginRequiredMixin, CreateView):
    model = Movie
    login_url = reverse_lazy('login')
    form_class = MovieForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(MovieCreateView, self).get_context_data()
        context['form']['studio'].field.empty_label = None
        return context


class MovieUpdateView(LoginRequiredMixin, UpdateView):
    model = Movie
    login_url = reverse_lazy('login')
    form_class = MovieForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form']['studio'].field.empty_label = None

        movie = Movie.objects.get(pk=self.kwargs['pk'])
        context['current'] = {
            'type': movie.type,
            'status': movie.status,
            'source': movie.source,
            'rating': movie.rating,
            'studio': movie.studio_id,
            'genres': movie.genre.all().values_list('pk', flat=True),
            'related': movie.related.all().values_list('pk', flat=True),
        }

        return context


class GenreModalView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.is_ajax:
            return HttpResponseForbidden()
        else:
            obj, created = Genre.objects.get_or_create(title=request.POST.get('title'))

        if created:
            return HttpResponse(f'{obj.pk},{obj.title}')

        return HttpResponse(created)


# TODO: delete if dont need it and clean urls
class GenreListView(View):
    http_method_names = ['get']

    def get(self, request):
        queryset = Genre.objects.all().only('title')
        data = serialize('json', Genre.objects.all(), fields='title')
        return JsonResponse(data, safe=False)


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


class StudioModalView(View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.is_ajax:
            return HttpResponseForbidden()
        else:
            obj, created = Studio.objects.get_or_create(name=request.POST.get('name'))

        if created:
            return HttpResponse(f'{obj.pk},{obj.name}')

        return HttpResponse(created)
