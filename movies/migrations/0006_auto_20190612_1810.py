# Generated by Django 2.2.2 on 2019-06-12 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_auto_20190612_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='related',
            name='main_movie',
        ),
        migrations.RemoveField(
            model_name='related',
            name='related_movies',
        ),
        migrations.AddField(
            model_name='related',
            name='movies',
            field=models.ManyToManyField(to='movies.Movie'),
        ),
    ]
