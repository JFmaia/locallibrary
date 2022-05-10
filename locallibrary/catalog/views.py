from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookModelForm
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

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

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Lista de exibição genérica baseada em classe listando livros emprestados ao usuário atual."""
    model = BookInstance
    template_name ='bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='e').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # Se esta for uma solicitação POST, então processe os dados do Formulário
    if request.method == 'POST':

        # Crie uma instância de formulário e preencha-a com dados da solicitação (vinculação):
        form = RenewBookForm(request.POST)

        # Verifique se o formulário é válido:
        if form.is_valid():
            # processe os dados em form.cleaned_data conforme necessário (aqui nós apenas escrevemos para o modelo due_back campo)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirecionar para uma nova URL:
            return HttpResponseRedirect(reverse('index'))

    # Se for um GET (ou qualquer outro método) crie o formulário padrão.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'book_renew_librarian.html', context)

class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}
    template_name ='author_form.html'

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name ='author_form.html'

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    template_name ='author_confirm_delete.html'
