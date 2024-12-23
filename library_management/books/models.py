from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    ISBN = models.CharField(max_length=13, unique=True)
    published_year = models.IntegerField()
    availability_status = models.IntegerField(default=1)

    def __str__(self):
        return self.title
