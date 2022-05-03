from django.db import models
from django.urls import reverse # Usado para gerar URLs invertendo os padrões de URL do Django

class Genre(models.Model):
    #representa o genero do livro!
    name = models.CharField(max_length=200, help_text='Digite um genero do livro (e.g. Science Fiction)')

    def __str__(self):
        return self.name

class Book(models.Model):
    """Modelo representando um livro (mas não uma cópia específica de um livro)."""
    title = models.CharField(max_length=200)

    # Chave Estrangeira usada porque livro só pode ter um autor, mas autores podem ter vários livros
    # Autor como uma sequência em vez de objeto porque ele ainda não foi declarado no arquivo.
    # on_delete=models.SET_NULL: se o autor for excluído, coloca null.
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Digite um resumo do livro')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">Numero ISBN</a>')

    # ManyToManyField usado porque o gênero pode conter muitos livros. Os livros podem cobrir muitos gêneros.
    # Classe de gênero já foi definida para que possamos especificar o objeto acima.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Retorna a url para acessar um registro de detalhes para este livro."""
        return reverse('book-detail', args=[str(self.id)])

