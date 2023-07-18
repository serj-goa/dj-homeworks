from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

import csv


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    page_number = int(request.GET.get('page', 1))

    db_path = settings.BUS_STATION_CSV
    data: list[dict] = load_data(db_path)
    
    paginator = Paginator(data, 10)
    page = paginator.get_page(page_number)

    context = {
        'bus_stations': page,
        'page': page,
    }
    return render(request, 'stations/index.html', context)


def load_data(db_path: str):
    with open(db_path, newline='') as csvfile:
        return list(csv.DictReader(csvfile))
