from django.urls import path

from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.MovieListView.as_view(), name='index'),
    path('<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('<int:pk>/favorite/', views.MovieToFavoriteView.as_view(), name='movie-favorite'),
    path('scores/', views.ScoreListView.as_view(), name='score-list'),
    path('<genre>/', views.MovieByGenreListView.as_view(), name='genre-detail'),
]
