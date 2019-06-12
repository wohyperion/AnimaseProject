from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import (Movie)


# Create your views here.
def index(request):
    context = {}
    return render(request, 'base.html', context)


class MovieListView(ListView):
    model = Movie
    paginate_by = 12


class MovieDetailView(DetailView):
    model = Movie
