from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic

def index(request):
    """Função view da home page do site."""

    # Pegando dados dos modelos book, BookInstance e author!
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Livros disponiveis (status = 'd')
    num_instances_available = BookInstance.objects.filter(status__exact='d').count()

    # A funcionalidade All() é implementada por default.
    num_authors = Author.objects.count()

    # Número de visitas a essa visão, conforme contado na variável sessão.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Renderização da página index.html com o contexto context disponivel.
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    context_object_name = 'book_list'  # seu próprio nome para a lista como uma variável de modelo
    queryset = model.objects.all()  # lista de 5 livros
    template_name = 'book_list.html'  # Especifique seu próprio nome/localização do modelo

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'

class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'  # seu próprio nome para a lista como uma variável de modelo
    queryset = model.objects.all()  # todos os autores
    template_name = 'author_list.html'  # Especifique seu próprio nome/localização do modelo

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author_detail.html'