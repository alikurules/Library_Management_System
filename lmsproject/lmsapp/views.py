from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Book, User, Transaction
from .serializers import BookSerializer, UserSerializer, TransactionSerializer
from django.core.exceptions import ValidationError

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] 


    # Custom action to handle checkout of a book
    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        book = self.get_object()

        # Try to fetch the user from the request data
        try:
            user = User.objects.get(id=request.data['user_id'])
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if there are available copies of the book
        if book.copies_available > 0:
            # Decrease the available copies and create a transaction
            try:
                transaction = Transaction.objects.create(user=user, book=book)
                book.copies_available -= 1
                book.save()
                return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'No copies available'}, status=status.HTTP_400_BAD_REQUEST)

    # Custom action to handle returning a book
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        book = self.get_object()

        # Try to find the active transaction for this book
        try:
            transaction = Transaction.objects.filter(book=book, return_date=None).first()
        except Transaction.DoesNotExist:
            return Response({'detail': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update the transaction's return date and increase available copies
        if transaction:
            try:
                transaction.return_date = request.data.get('return_date', None)
                transaction.save()

                book.copies_available += 1
                book.save()

                return Response(TransactionSerializer(transaction).data, status=status.HTTP_200_OK)
            except ValidationError as e:
                return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'No active transaction found'}, status=status.HTTP_404_NOT_FOUND)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            # Check if the user already exists before creating a new one
            if User.objects.filter(email=request.data.get('email')).exists():
                return Response({'detail': 'A user with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.data['user'])
            book = Book.objects.get(id=request.data['book'])

            # Check if there are available copies before allowing the transaction
            if book.copies_available <= 0:
                return Response({'detail': 'No available copies to check out.'}, status=status.HTTP_400_BAD_REQUEST)

            return super().create(request, *args, **kwargs)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Book.DoesNotExist:
            return Response({'detail': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

