from django.db import models


# Create your models here.
class Genre(models.Model):
    pass


class Studio(models.Model):
    pass


class Movie(models.Model):
    """
    Represent anime
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
    episodes = models.PositiveSmallIntegerField(help_text='Enter a number of episodes')
    status = models.CharField(max_length=15, choices=STATUSES,
                              help_text='Choice the current status of (e.g. Completed or not, announced)')
    release_date = models.DateField(null=True, blank=True, help_text='Date of announce or first episode release')
    # TODO: Movie.end_date check end_date > release_date
    end_date = models.DateField(null=True, blank=True,
                                help_text='Project closing date or date of last episode release')
    source = models.CharField(max_length=10, choices=SOURCES,
                              help_text='The type of resource that became the basis of current anime')
    # TODO: Movie.duration check duration > 0
    duration = models.PositiveSmallIntegerField(help_text='Duration of episode in minutes')
    rating = models.CharField(max_length=30, choices=RATINGS, help_text='Choice MPAA film rating')
    studio = models.ForeignKey(Studio, on_delete=models.SET_NULL, null=True, blank=True,
                               help_text='Select the studio that released that anime')
    genre = models.ManyToManyField(Genre, help_text='Select the genres')
    summary = models.TextField(max_length=1000, help_text='Enter a summary')
    # TODO: Movie.cover_url check resource response before save
    cover_url = models.URLField(help_text='Enter a cover URL address')
    # TODO: Movie.trailer_url check youtube.com domain
    trailer_url = models.URLField(help_text='Enter a YouTube video trailer URL')


class Score(models.Model):
    pass


class Comment(models.Model):
    pass


class Favorite(models.Model):
    pass


class Related(models.Model):
    pass
