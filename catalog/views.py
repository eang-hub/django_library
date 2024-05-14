from django.http import Http404

from .models import Book, Author, BookInstance, Genre
from django.shortcuts import render
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from .forms import RenewBookForm


class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'  # your own name for the list as a template variable
    queryset = Book.objects.all()  # Get 5 books containing the title war
    paginate_by = 1
    template_name = 'books/book_list.html'  # Specify your own template name/location


class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/book_detail.html'  # Specify your own template name/location


class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'  # your own name for the list as a template variable
    queryset = Author.objects.all()  # Get 5 books containing the title war
    template_name = 'author/author_list.html'  # Specify your own template name/location


class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author/author_detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name = 'books/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


# def book_detail_view(request,pk):
#     try:
#         book_id=Book.objects.get(pk=pk)
#     except Book.DoesNotExist:
#         raise Http404("Book does not exist")
#
#     #book_id=get_object_or_404(Book, pk=pk)
#
#     return render(
#         request,
#         'book/book_detail.html',
#         context={'book':book_id,}
#     )

class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'books/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@login_required  # 如果已登陆将正常执行
def index(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # 生成一些主要对象的计数
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # 可用书籍（状态 = 'a'）
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # 默认情况下，'all()'是隐含的。

    # 使用上下文变量中的数据呈现带有HTML模板index.html
    return render(
        request,
        'index.html',
        context={'num_books': num_books,
                 'num_instances': num_instances,
                 'num_instances_available': num_instances_available,
                 'num_authors': num_authors,
                 'num_visits': num_visits
                 },
    )


def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date, })

    return render(request, 'books/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018', }
    template_name = 'books/author_form.html'


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name = 'books/author_form.html'


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    template_name = 'books/author_confirm_delete.html'
