from django.db import models


class Book(models.Model):
    title = models.CharField(unique=True, max_length=100)
    author = models.CharField(max_length=100)
    published_year = models.IntegerField()
    no_of_pages = models.IntegerField()
    isbn = models.CharField(max_length=13)
    cover = models.ImageField(upload_to='images/')
    pdf = models.FileField(upload_to='files/')

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ('title',)
