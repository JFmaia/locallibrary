from django.db import models

class Genre(models.Model):
    #representa o genero do livro!
    name = models.CharField(max_length=200, help_text='Digite um genero do livro (e.g. Science Fiction)')

    def __str__(self):
        return self.name
