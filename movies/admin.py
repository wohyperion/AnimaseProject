from django.contrib import admin

from . import models

admin.site.register(models.Genre)
admin.site.register(models.Studio)
admin.site.register(models.Movie)
admin.site.register(models.Score)
admin.site.register(models.Favorite)
