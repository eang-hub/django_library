from django.db import models
from django.urls import reverse # 用于通过反向URL模式生成URL
import uuid # 用于唯一书籍实例的必需项


# python manage.py makemigrations
# python manage.py migrate


class Genre(models.Model):
    """
    表示书籍流派的模型（例如科幻、非虚构等）。
    """
    name = models.CharField(max_length=200, help_text="输入书籍流派（例如科幻、法国诗歌等）")

    def __str__(self):
        """
        用于表示模型对象的字符串（在管理站点中等）。
        """
        return self.name

class Book(models.Model):
    """
    表示一本书的模型（但不是书的具体副本）。
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # 外键用于书只能有一个作者，但作者可以有多本书
    # 作者作为字符串而不是对象，因为文件中尚未声明
    summary = models.TextField(max_length=1000, help_text="输入书的简要描述")
    isbn = models.CharField('ISBN',max_length=13, help_text='13 位字符的 <a href="https://www.isbn-international.org/content/what-isbn">ISBN 号码</a>')
    genre = models.ManyToManyField(Genre, help_text="选择该书的流派")
    # 由于流派可以包含多本书，因此使用 ManyToManyField。书籍可以涵盖多种流派。
    # 流派类已经定义，因此我们可以在上面指定对象。

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def __str__(self):
        """
        用于表示模型对象的字符串。
        """
        return self.title


    def get_absolute_url(self):
        """
        返回访问特定书籍实例的URL。
        """
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    """
    表示一本书的具体副本（即可以从图书馆借阅的书籍）。
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="整个图书馆中此特定书籍的唯一 ID")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', '维护中'),
        ('o', '已借出'),
        ('a', '可用'),
        ('r', '预约'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='书的可用性')

    class Meta:
        ordering = ["due_back"]


    def __str__(self):
        """
        用于表示模型对象的字符串
        """
        return '%s (%s)' % (self.id,self.book.title)

class Author(models.Model):
    """
    表示作者的模型。
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('死亡日期', null=True, blank=True)

    def get_absolute_url(self):
        """
        返回访问特定作者实例的URL。
        """
        return reverse('author-detail', args=[str(self.first_name)])

    def __str__(self):
        """
        用于表示模型对象的字符串。
        """
        return '%s, %s' % (self.last_name, self.first_name)



