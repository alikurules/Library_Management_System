from django.contrib import admin
from .models import User, Book

# Register User model
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'date_of_membership', 'is_active']
    search_fields = ['username', 'email']

# Register Book model
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'published_date', 'copies_available']
    search_fields = ['title', 'author', 'isbn']
    list_filter = ['published_date']

