from django.db import models

# Create your models here.


from django.db import models


class Book(models.Model):
    book_id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    available = models.BooleanField(default=True, null=True)

    class Meta:
        db_table = 'books'
        managed = False

    def __str__(self):
        return self.title

class IssuedBook(models.Model):
    issue_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=20)
    book_id = models.CharField(max_length=20)
    issue_date = models.DateField()
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'issued_books'
        managed = False