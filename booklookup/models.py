
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=300)
    authors = models.CharField(max_length=300)
    isbn_10 = models.CharField(max_length=20, blank=True, null=True)
    isbn_13 = models.CharField(max_length=20, blank=True, null=True)
    asin = models.CharField(max_length=20, blank=True, null=True)
    source = models.CharField(max_length=100)
    price = models.CharField(max_length=20, blank=True, null=True)
    purchase_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} by {self.authors}"
