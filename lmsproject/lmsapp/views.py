from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.utils.timezone import now
from django.contrib.auth import get_user_model

from .models import Book, Transaction
from .serializers import UserSerializer, BookSerializer, TransactionSerializer

User = get_user_model()

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        """Ensure no duplicate usernames or emails"""
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": "Failed to create user. Ensure username and email are unique."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'author', 'isbn']
    pagination_class = CustomPagination

    def create(self, request, *args, **kwargs):
        """Handle duplicate ISBN error gracefully"""
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response(
                {"error": "Failed to create book. ISBN must be unique."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=['get'], url_path='available')
    def available_books(self, request):
        """Get books with available copies"""
        try:
            available_books = Book.objects.filter(available_copies__gt=0)
            page = self.paginate_queryset(available_books)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return Response(
                {"error": "Failed to fetch available books."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='checkout')
    def checkout(self, request):
        """Checkout a book"""
        user = request.user
        book_id = request.data.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
            if book.available_copies > 0:
                book.available_copies -= 1
                book.save()
                transaction = Transaction.objects.create(user=user, book=book)
                return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
            return Response({"error": "No available copies."}, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": "Failed to checkout book."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=['post'], url_path='return')
    def return_book(self, request):
        """Return a checked-out book"""
        user = request.user
        transaction_id = request.data.get('transaction_id')
        try:
            transaction = Transaction.objects.get(id=transaction_id, user=user, return_date__isnull=True)
            transaction.return_date = now()
            transaction.book.available_copies += 1
            transaction.book.save()
            transaction.save()
            return Response(TransactionSerializer(transaction).data, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found or already returned."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(
                {"error": "Failed to return book."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
