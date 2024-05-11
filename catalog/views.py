from django.http import Http404

from .models import Book, Author, BookInstance, Genre
from django.shortcuts import render
from django.views import generic

class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'   # your own name for the list as a template variable
    queryset = Book.objects.all() # Get 5 books containing the title war
    paginate_by = 1
    template_name = 'books/book_list.html'  # Specify your own template name/location

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/book_detail.html'  # Specify your own template name/location

class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'   # your own name for the list as a template variable
    queryset = Author.objects.all() # Get 5 books containing the title war
    template_name = 'author/author_list.html'  # Specify your own template name/location



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

def index(request):
    """
    网站首页的视图函数。
    """
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
        context={'num_books': num_books, 'num_instances': num_instances, 'num_instances_available': num_instances_available, 'num_authors': num_authors},
    )
