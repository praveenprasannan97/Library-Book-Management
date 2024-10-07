from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    country = models.CharField(max_length=100)

    class Meta:
        permissions = [
            ('can_add_author', 'Can add author'),
            ('can_list_author', 'Can list author'),
            ('can_edit_author', 'Can edit author'),
            ('can_delete_author', 'Can delete author'),
        ]

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    ISBN = models.CharField(max_length=13, unique=True)
    authors = models.ManyToManyField('Author')
    publication_date = models.DateField()
    copies_available = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=[('available', 'Available'), ('borrowed', 'Borrowed')], default='available')

    class Meta:
        permissions = [
            ('can_list_book', 'Can list book'),
            ('can_add_book', 'Can add book'),
            ('can_edit_book', 'Can edit book'),
            ('can_delete_book', 'Can delete book'),
            ('can_borrow_book', 'Can borrow book'),
            ('can_return_book', 'Can return book'),
        ]

    def __str__(self):
        return self.title
    
class BorrowingHistory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('borrowed', 'Borrowed'), ('returned', 'Returned')], default='borrowed')

    class Meta:
        permissions = [
            ('can_view_history', 'Can view History'),
            ('can_edit_history', 'Can edit History'),
        ]

    def __str__(self):
        return f'{self.user} borrowed {self.book}'