# Generated by Django 2.2.2 on 2019-06-12 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_auto_20190612_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='related',
            field=models.ManyToManyField(help_text='Choose related anime', related_name='_movie_related_+', to='movies.Movie'),
        ),
        migrations.DeleteModel(
            name='Related',
        ),
    ]
