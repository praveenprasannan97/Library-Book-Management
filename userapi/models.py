from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    ISBN = models.CharField(max_length=13, unique=True)
    authors = models.ManyToManyField('Author')
    publication_date = models.DateField()
    copies_available = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=[('available', 'Available'), ('borrowed', 'Borrowed')], default='available')

    def __str__(self):
        return self.title
    
class BorrowingHistory(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[('borrowed', 'Borrowed'), ('returned', 'Returned')], default='borrowed')

    def __str__(self):
        return f'{self.user} borrowed {self.book}'