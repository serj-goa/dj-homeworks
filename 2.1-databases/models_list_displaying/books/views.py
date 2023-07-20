from django.shortcuts import render

from .models import Book


def book_detail_view(request, pub_date):
    template = 'books/book_detail.html'
    book = Book.objects.filter(pub_date=pub_date)[0]

    previous_page = Book.objects.filter(pub_date__lt=pub_date).values('pub_date').first()
    previous_page = previous_page['pub_date'].strftime('%Y-%m-%d') if previous_page else None

    next_page = Book.objects.filter(pub_date__gt=pub_date).values('pub_date').first()
    next_page = next_page['pub_date'].strftime('%Y-%m-%d') if next_page else None

    context = {
        'book': book,
        'previous_page': previous_page,
        'next_page': next_page,
    }

    return render(request, template, context)


def books_view(request):
    template = 'books/books_list.html'

    books = Book.objects.all()
    context = {'books': books}

    return render(request, template, context)
