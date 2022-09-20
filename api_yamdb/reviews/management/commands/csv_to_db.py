import csv
import os
import sys

from django.core.management import BaseCommand
from reviews.models import (Category, Comments, Genre, GenreTitle, Review,
                            Title, User)

from api_yamdb.settings import CSV_DIR

FILENAMES_AND_MODELS = {
    'users': User,
    'category': Category,
    'genre': Genre,
    'titles': Title,
    'review': Review,
    'comments': Comments,
    'genre_title': GenreTitle,
}

FIELDS = {
    'author': ('author', User),
    'category': ('category', Category),
    'genre_id': ('genre', Genre),
    'title_id': ('title', Title),
    'review_id': ('review', Review),
}


def open_file(filename):
    file = filename + '.csv'
    path = os.path.join(CSV_DIR, file)
    with (open(path, encoding='utf-8')) as file:
        return list(csv.reader(file))


def change_foreign_values(data):
    copy_data = data.copy()
    for field_key, field_value in data.items():
        if field_key in FIELDS.keys():
            field_key0 = FIELDS[field_key][0]
            copy_data[field_key0] = FIELDS[field_key][1].objects.get(
                pk=field_value)
    return copy_data


def load(filename, model):
    data = open_file(filename)
    rows = data[1:]
    for row in rows:
        data_csv = dict(zip(data[0], row))
        data_csv = change_foreign_values(data_csv)
        try:
            table = model(**data_csv)
            table.save()
        except ValueError:
            sys.stdout.write('ValueError while loading\n')
            break
    sys.stdout.write('Data loaded successfully\n')


class Command(BaseCommand):

    def handle(self, *args, **options):

        for key, value in FILENAMES_AND_MODELS.items():
            sys.stdout.write(f'Data for {key} loading\n')
            load(key, value)
