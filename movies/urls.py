from django.urls import path

from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.MovieListView.as_view(), name='index'),
    path('allowed/', views.MovieByAllowedListVew.as_view(), name='movie-allowed'),
    path('<int:pk>/publish/', views.MovieShowView.as_view(), name='movie-set-allow'),
    path('<int:pk>/hide/', views.MovieHideView.as_view(), name='movie-hide'),
    path('<int:pk>/score/', views.ScoreCreateView.as_view(), name='score-create'),
    path('create/', views.MovieCreateView.as_view(), name='movie-create'),
    path('<int:pk>/edit/', views.MovieUpdateView.as_view(), name='movie-update'),
    path('<int:pk>/delete/', views.MovieDeleteView.as_view(), name='movie-delete'),
    path('<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('<int:pk>/favorite/', views.MovieFavoriteView.as_view(), name='movie-favorite'),
    path('scores/', views.ScoreListView.as_view(), name='score-list'),
    path('genres/create/', views.GenreModalView.as_view(), name='genre-create'),
    path('studios/create/', views.StudioModalView.as_view(), name='studio-create'),
    path('user/', views.UserDetailView.as_view(), name='user-detail'),
    path('<genre>/', views.MovieByGenreListView.as_view(), name='genre-detail'),
]
