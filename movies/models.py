from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Genre(models.Model):
    """
    Describe genre for movie
    """

    # Fields
    title = models.CharField(max_length=100, help_text='Enter genre title (Action, Horror, etc.)')
    description = models.TextField(max_length=500, null=True, blank=True,
                                   help_text='Enter description of genre or leave it blank')

    # Methods
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movies:genre-detail', kwargs={'pk': self.pk})


class Studio(models.Model):
    """
    Represent studio
    """

    # Fields
    name = models.CharField(max_length=100, help_text='Enter studio name')

    # Methods
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movies:studio-detail', kwargs={'pk': self.pk})


class Movie(models.Model):
    """
    Represent movie item (anime)
    """

    # Constants
    TYPES = (
        ('T', 'TV'),
        ('M', 'Movie'),
        ('O', 'OVA'),
        ('S', 'Special')
    )
    STATUSES = (
        ('C', 'Completed'),
        ('N', 'Not completed'),
        ('A', 'Announced')
    )
    SOURCES = (
        ('M', 'Manga'),
        ('G', 'Game'),
        ('N', 'Novel'),
        ('O', 'Original')
    )
    RATINGS = (
        ('G', 'General audiences'),
        ('PG', 'Parental guidance suggested'),
        ('PG-13', 'Parents strongly cautioned'),
        ('R', 'Restricted'),
        ('NC-17', 'No One 17 & Under Admitted')
    )

    # Fields
    title = models.CharField(max_length=200, help_text='Enter a title of anime')
    synonym = models.CharField(max_length=200, help_text='Enter a title synonym (e.g. Japanese title)', blank=True,
                               null=True)
    type = models.CharField(max_length=10, choices=TYPES,
                            help_text='Choice a type of anime (TV, Movie, OVA or Special)')
    # TODO: Movie.episodes check episodes > 0
    episodes = models.PositiveSmallIntegerField(help_text='Enter a number of episodes', default=12)
    status = models.CharField(max_length=15, choices=STATUSES,
                              help_text='Choice the current status of (e.g. Completed or not, announced)')
    release_date = models.DateField(null=True, blank=True, help_text='Date of announce or first episode release')
    # TODO: Movie.end_date check end_date > release_date
    end_date = models.DateField(null=True, blank=True,
                                help_text='Project closing date or date of last episode release')
    source = models.CharField(max_length=10, choices=SOURCES,
                              help_text='The type of resource that became the basis of current anime')
    # TODO: Movie.duration check duration > 0
    duration = models.PositiveSmallIntegerField(help_text='Duration of episode in minutes', default=23)
    rating = models.CharField(max_length=30, choices=RATINGS, help_text='Choice MPAA film rating', default='R')
    studio = models.ForeignKey(Studio, on_delete=models.SET_NULL, null=True, blank=True,
                               help_text='Select the studio that released that anime')
    genre = models.ManyToManyField(Genre, help_text='Select the genres')
    summary = models.TextField(max_length=1000, help_text='Enter a summary', null=True, blank=True)
    # TODO: Movie.cover_url check resource response before save
    cover_url = models.URLField(help_text='Enter a cover URL address', blank=True, null=True)
    # TODO: Movie.trailer_url check youtube.com domain
    trailer_url = models.URLField(help_text='Enter a YouTube video trailer URL', null=True, blank=True)

    # Methods
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movies:movie-detail', kwargs={'pk': self.pk})


class Score(models.Model):
    """
    User can set a score and leave a comment
    """

    # Fields
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # TODO: Score.value check: 0 < value <= 10
    value = models.PositiveSmallIntegerField(help_text='Enter your score')
    message = models.TextField(max_length=500, help_text='Justify your opinion', null=True, blank=True)

    # Methods
    def __str__(self):
        # TODO: make readable str representation
        return self.movie.title

    def get_absolute_url(self):
        return reverse('movies:score-detail', kwargs={'pk': self.pk})


class Favorite(models.Model):
    """
    User can add liked movie to favorites list
    """

    # Fields
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # TODO: try ManyToManyField
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Methods
    def __str__(self):
        # TODO: make readable str representation
        return self.movie.title

    def get_absolute_url(self):
        return reverse('movies:favorite-detail', kwargs={'pk': self.pk})


class Related(models.Model):
    """
    Show relation between movies
    """

    # Fields
    main_movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='main_movie')
    # TODO: check main_movie != relate_movies
    related_movies = models.ManyToManyField(Movie, related_name='related_movies')

    # Methods
    def __str__(self):
        return self.main_movie.title

    def get_absolute_url(self):
        return reverse('movies:related-detail', kwargs={'pk': self.pk})
