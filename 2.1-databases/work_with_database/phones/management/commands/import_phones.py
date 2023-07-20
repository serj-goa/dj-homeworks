import csv

from django.core.management.base import BaseCommand
from phones.models import Phone


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('phones.csv', 'r') as file:
            phones = list(csv.DictReader(file, delimiter=';'))

        for phone in phones:
            # name, price, image, release_date, lte_exists и slug
            # id;name;image;price;release_date;lte_exists

            Phone.objects.create(
                name=phone['name'],
                price=phone['price'],
                image=phone['image'],
                release_date=phone['release_date'],
                lte_exists=phone['lte_exists'],
                slug=convert_to_slug(phone['name']),
            )


def convert_to_slug(text: str) -> str:
    text = text.lower().replace(' ', '_').replace('&', '_and_')
    return text
