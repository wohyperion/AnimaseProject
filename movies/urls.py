from django.urls import path

from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.MovieListView.as_view(), name='index'),
    path('<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('scores/', views.ScoreListView.as_view(), name='score-list'),
    path('<genre>/', views.GenreMovieListView.as_view(), name='genre-detail'),
]
