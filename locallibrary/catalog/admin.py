from django.contrib import admin
from catalog.models import Author, Genre, Book, BookInstance, Language

# Registrando os odelos aqui.
# Definindo a classe Author com o decorador @admin.register
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

# Registre as aulas de Administração para Livro usando o decorador
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

# Registre as classes de administração para BookInstance usando o decorador
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')

admin.site.register(Genre)
admin.site.register(Language)