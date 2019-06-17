from django.urls import path

from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.MovieListView.as_view(), name='index'),
    path('create/', views.MovieCreateView.as_view(), name='movie-create'),
    path('<int:pk>/edit/', views.MovieUpdateView.as_view(), name='movie-update'),
    path('<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('<int:pk>/favorite/', views.FavoriteMovieView.as_view(), name='movie-favorite'),
    path('scores/', views.ScoreListView.as_view(), name='score-list'),
    path('genres/', views.GenreListView.as_view(), name='genre-list'),
    path('genres/create/', views.GenreModalView.as_view(), name='genre-create'),
    path('studios/create/', views.StudioModalView.as_view(), name='studio-create'),
    path('<genre>/', views.MovieByGenreListView.as_view(), name='genre-detail'),
]
