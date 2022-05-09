from django.db import models
from django.urls import reverse # Usado para gerar URLs invertendo os padrões de URL do Django
import uuid # Required for unique book instances
from django.contrib.auth.models import User
from datetime import date

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
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Retorna a url para acessar um registro de detalhes para este livro."""
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        """Criando a string para o genero. Isso é requerido para o display genre no Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    """Modelo representando uma cópia específica de um livro (ou seja, que pode ser emprestado da biblioteca)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='ID exclusivo para este livro específico em toda a biblioteca')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Manutenção'),
        ('e', 'Em emprestimo'),
        ('d', 'Disponivel'),
        ('i', 'Indisponivel'),
        ('r', 'Reservado'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Disponibilidade do livro',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """Retorna uma string que representa o livro."""
        return f'{self.id} ({self.book.title})'
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

class Author(models.Model):
    """Esse model representa o autor do livro"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Retorna a url para acessar um registro de detalhes do autor."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """Retorna uma string que representa o autor."""
        return f'{self.last_name}, {self.first_name}'

class Language(models.Model):
    """Modelo representando um idioma (por exemplo, inglês, francês, japonês etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Insira o idioma natural do livro (por exemplo, inglês, francês, japonês etc.)")

    def __str__(self):
        return self.name