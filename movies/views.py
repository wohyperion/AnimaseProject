from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.core.serializers import serialize
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from .models import (Movie, Genre, Score, Favorite, Studio)
from .forms import (MovieForm, ScoreForm, UserForm)


# General website page [index]
class MovieListView(ListView):
    model = Movie
    paginate_by = 24
    ordering = ['-added_date']

    def get_context_data(self, **kwargs):
        context = super(MovieListView, self).get_context_data()
        context['genre_list'] = Genre.objects.all()
        return context


# Detailed movie page [movie-detail]
class MovieDetailView(DetailView):
    model = Movie

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().allowed and not self.request.user.is_superuser and not self.request.user.has_perm(
                'movies.can_toggle_allowed'):
            return redirect('movies:index')

        return super(MovieDetailView, self).dispatch(request=request)

    def get_context_data(self, **kwargs):
        context = super(MovieDetailView, self).get_context_data()
        score_form = ScoreForm()

        try:
            favorite = Favorite.objects.get(movie_id=self.kwargs['pk'], user_id=self.request.user.pk)
        except Favorite.DoesNotExist:
            favorite = None

        context['favorite'] = favorite
        context['score_form'] = score_form

        if self.request.user.is_authenticated:
            context['score_exist'] = Score.score_exist(movie=self.object, user=self.request.user)
        else:
            context['score_exist'] = True

        return context


# Movie filter by genres. General access from index page [genre-detail]
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


# Administrators and creators page for publication movies which added by usual user [movie-allowed]
class MovieByAllowedListVew(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Movie
    paginate_by = 24
    template_name = 'movies/movie_by_allowed.html'
    ordering = ['-added_date']
    login_url = reverse_lazy('login')
    permission_required = ['movies.can_toggle_allowed']
    permission_denied_message = 'You\'r should be creator!'

    def get_queryset(self):
        return Movie.objects.filter(allowed=False)


# Endpoint for set True to allowed status of movie [movie-set-allow]
class MovieShowView(LoginRequiredMixin, PermissionRequiredMixin, View):
    http_method_names = ['post']
    login_url = reverse_lazy('login')
    permission_required = ['movies.can_toggle_allowed']
    permission_denied_message = 'You\'r should be creator!'

    @staticmethod
    def post(request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            movie.allowed = True
            movie.save()
            if request.is_ajax():
                return JsonResponse({
                    'success': True
                })
            else:
                return redirect('movies:movie-allowed')
        except ObjectDoesNotExist as error:
            raise error


# Endpoint for set False to allowed status of movie [movie-hide]
class MovieHideView(LoginRequiredMixin, PermissionRequiredMixin, View):
    http_method_names = ['post']
    login_url = reverse_lazy('login')
    permission_required = ['movies.can_toggle_allowed']
    permission_denied_message = 'You\'r should be creator!'

    @staticmethod
    def post(request, pk):
        try:
            movie = Movie.objects.get(pk=pk)
            movie.allowed = False
            movie.save()
            return JsonResponse({
                'success': True,
                'url': reverse('movies:index')
            })
        except ObjectDoesNotExist as error:
            raise error


# Page for adding a new movie to site [movie-create]
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


# Based on MovieCreateView page for updating movie information [movie-update]
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

    def get_object(self, queryset=None):
        obj = super(MovieUpdateView, self).get_object()

        if obj.user == self.request.user or self.request.user.has_perm('movies.can_toggle_allowed'):
            return obj

        raise PermissionDenied()


# Delete movies view [movie-delete]
class MovieDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Movie
    login_url = reverse_lazy('login')
    permission_required = ['movies.can_toggle_allowed']
    permission_denied_message = 'You\'r should be creator!'
    success_url = reverse_lazy('movies:index')


# Endpoint for create new genres on MovieCreateView/MovieUpdateView pages [genre-create]
class GenreModalView(View):
    http_method_names = ['post']

    @staticmethod
    def post(request):
        if not request.user.is_authenticated and not request.is_ajax():
            return HttpResponseForbidden()
        else:
            obj, created = Genre.objects.get_or_create(title=request.POST.get('title'))

        if created:
            return HttpResponse(f'{obj.pk},{obj.title}')

        return HttpResponse(created)


# A list of all latest scores [score-list]
class ScoreListView(ListView):
    model = Score
    paginate_by = 24
    ordering = ['-date']


class ScoreCreateView(LoginRequiredMixin, View):
    http_method_names = ['post']
    login_url = reverse_lazy('login')

    @staticmethod
    def post(request, pk):
        form = ScoreForm(request.POST)

        try:
            if form.is_valid():
                movie = Movie.objects.get(pk=pk)
                user = User.objects.get(pk=request.user.pk)
                score = Score(
                    movie=movie,
                    user=user,
                    value=form.cleaned_data.get('value'),
                    message=form.cleaned_data.get('message')
                )
                score.save()
                return redirect('movies:movie-detail', pk)
        except ObjectDoesNotExist as error:
            raise error


# Endpoint for adding favorite movies to user profile [movie-favorite]
class MovieFavoriteView(View):
    http_method_names = ['post']

    @staticmethod
    def post(request, pk):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        if get_object_or_404(Movie, pk=pk):
            obj, created = Favorite.objects.get_or_create(
                movie_id=pk,
                user_id=request.user.pk
            )

            if not created:
                obj.delete()

            return HttpResponse(created)


# Endpoint for create new studios on MovieCreateView/MovieUpdateView pages [studio-create]
class StudioModalView(View):
    http_method_names = ['post']

    @staticmethod
    def post(request):
        if not request.user.is_authenticated and not request.is_ajax():
            return HttpResponseForbidden()
        else:
            obj, created = Studio.objects.get_or_create(name=request.POST.get('name'))

        if created:
            return HttpResponse(f'{obj.pk},{obj.name}')

        return HttpResponse(created)


class UserDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'movies/user_detail.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data()
        user = self.request.user

        context['user'] = user

        return context


class SignUpView(FormView):
    form_class = UserForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'),
                email=form.cleaned_data.get('email')
            )
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()

        return redirect('login')
