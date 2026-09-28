from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=100, verbose_name="Artista")

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Género Musical")

    def __str__(self):
        return self.name

class Album(models.Model):
    title = models.CharField(max_length=150, verbose_name="Álbum")
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name="Artista")
    year = models.IntegerField(verbose_name="Año")
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Género")
    image = models.ImageField(upload_to='music/', blank=True, null=True, verbose_name="Carátula")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    price = models.IntegerField(verbose_name="Precio ($CLP)")

    def __str__(self):
        return self.title