from rest_framework import serializers
from .models import Book


class BookSerializer(serializers. HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ('url', 'id', 'title', 'author', 'published_year', 'isbn', 'no_of_pages', 'cover', 'pdf')
