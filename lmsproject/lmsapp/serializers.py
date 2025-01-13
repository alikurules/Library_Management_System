from rest_framework import serializers
from .models import Book, User, Transaction

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    # Custom validation for ISBN to ensure uniqueness
    def validate_isbn(self, value):
        if not value.isdigit() or len(value) != 13:
            raise serializers.ValidationError("ISBN must be a 13-digit number.")
        return value

    # Custom validation to check that the number of copies is non-negative
    def validate_copies_available(self, value):
        if value < 0:
            raise serializers.ValidationError("Number of available copies cannot be negative.")
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    # Custom validation to ensure the email is unique and valid
    def validate_email(self, value):
        if '@' not in value:
            raise serializers.ValidationError("Please enter a valid email address.")
        return value

class TransactionSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)  # Display book details in the transaction
    user = UserSerializer(read_only=True)  # Display user details in the transaction

    class Meta:
        model = Transaction
        fields = '__all__'

    # Custom validation to ensure that the book is not checked out if no copies are available
    def validate(self, data):
        book = data['book']
        if book.copies_available <= 0:
            raise serializers.ValidationError("No available copies to check out.")
        return data
