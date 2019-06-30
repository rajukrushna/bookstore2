from rest_framework import serializers
from .models import Book
from django.contrib.auth.models import User


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ('url', 'id', 'title', 'author', 'published_year', 'isbn', 'no_of_pages', 'cover', 'pdf')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')


class BookFieldsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'published_year', 'isbn', 'no_of_pages')


class BookCoverUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'cover')


class BookPdfUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'pdf')


class BookSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'published_year', 'isbn', 'no_of_pages', 'cover', 'pdf')
