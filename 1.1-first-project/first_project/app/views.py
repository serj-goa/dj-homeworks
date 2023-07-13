import os

from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, reverse


def home_view(request):
    template_name = 'app/home.html'
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir'),
    }
    context = {
        'pages': pages
    }

    return render(request, template_name, context)


def time_view(request):
    current_time = datetime.now().strftime('%X %A %d %B %Y')
    msg = f'Текущее время: {current_time}'

    return HttpResponse(msg)


def workdir_view(request):
    current_list_dir = ''

    for row in os.listdir(os.getcwd()):
        current_list_dir += f'<li>{row}</li>'

    return HttpResponse(
        f'<p>Current workdir list:</p>'
        f'<ul style="list-style:none">{current_list_dir}</ul>'
    )
