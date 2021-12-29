from django.db import models
from django.urls import reverse_lazy


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name='games')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy('game-details', args=(self.id, ))


class GameImage(models.Model):
    game = models.ForeignKey(Game,
                             on_delete=models.CASCADE,
                             related_name='images')
    image = models.ImageField(upload_to='games')
