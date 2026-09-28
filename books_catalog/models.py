from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Autor")

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Género")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=150, verbose_name="Título")
    # Relación ForeignKey: Permite seleccionar un autor existente o crear uno nuevo desde el Admin
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Autor")
    year = models.IntegerField(verbose_name="Año")
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Género")
    image = models.ImageField(upload_to='books/', blank=True, null=True, verbose_name="Portada")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    price = models.IntegerField(verbose_name="Precio ($CLP)")

    def __str__(self):
        return self.title