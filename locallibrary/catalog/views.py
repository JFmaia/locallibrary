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

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Renderize o modelo HTML index.html com os dados na variável de contexto
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'my_book_list'  # seu próprio nome para a lista como uma variável de modelo

    def get_queryset(self):
        return Book.objects.filter(title__icontains='Dom')[:5] # Obtenha 5 livros contendo o título 'Dom'

    def get_context_data(self, **kwargs):
        # Chame a implementação base primeiro para obter o contexto
        context = super(BookListView, self).get_context_data(**kwargs)
        # Crie quaisquer dados e adicione-os ao contexto
        context['some_data'] = 'This is just some data'
        return context
        
    template_name = 'books/my_arbitrary_template_name_list.html'  # Especifique seu próprio nome/localização do modelo