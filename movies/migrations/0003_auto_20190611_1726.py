# Generated by Django 2.2.2 on 2019-06-11 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20190611_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='cover_url',
            field=models.URLField(blank=True, help_text='Enter a cover URL address', null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='trailer_url',
            field=models.URLField(blank=True, help_text='Enter a YouTube video trailer URL', null=True),
        ),
    ]
