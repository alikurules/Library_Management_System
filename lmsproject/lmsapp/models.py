from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    copies_available = models.PositiveIntegerField()

    def clean(self):
        # Custom validation to ensure that the book has a positive number of copies available
        if self.copies_available < 0:
            raise ValidationError({'copies_available': 'Number of available copies cannot be negative.'})

    def save(self, *args, **kwargs):
        try:
            self.clean()  # Perform custom validation
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e  # Reraise the validation error for handling in views

    def __str__(self):
        return self.title

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    date_of_membership = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def clean(self):
        # Custom validation to ensure that the email follows the proper format
        if not self.email:
            raise ValidationError({'email': 'Email cannot be empty.'})
        if User.objects.filter(email=self.email).exists():
            raise ValidationError({'email': 'A user with this email already exists.'})

    def save(self, *args, **kwargs):
        try:
            self.clean()  # Perform custom validation
            super().save(*args, **kwargs)
        except ValidationError as e:
            raise e  # Reraise the validation error for handling in views

    def __str__(self):
        return self.username

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    checkout_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def clean(self):
        # Custom validation to ensure a book isn't checked out if no copies are available
        if self.book.copies_available <= 0:
            raise ValidationError({'book': 'No available copies left for checkout.'})

    def save(self, *args, **kwargs):
        try:
            self.clean()  # Perform custom validation
            super().save(*args, **kwargs)
            if not self.return_date:  # If the transaction is not returned, reduce book copies
                self.book.copies_available -= 1
                self.book.save()
        except ValidationError as e:
            raise e  # Reraise the validation error for handling in views

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

# Signals to handle updates to the number of copies
@receiver(post_save, sender=Transaction)
def update_book_copies(sender, instance, created, **kwargs):
    if instance.return_date:
        # If a transaction is marked as returned, increase the book copies
        instance.book.copies_available += 1
        instance.book.save()

@receiver(pre_save, sender=Transaction)
def check_out_book(sender, instance, **kwargs):
    if instance.return_date is None:
        # Before saving a transaction, ensure that there is at least one copy available
        if instance.book.copies_available <= 0:
            raise ValidationError({'book': 'No available copies left to check out.'})
