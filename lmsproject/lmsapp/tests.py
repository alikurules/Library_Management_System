from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book, LibraryUser, BorrowedBook

User = get_user_model()

class BookTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'published_date': '2023-01-01',
            'number_of_copies_available': 5
        }
        self.book = Book.objects.create(**self.book_data)

    def test_create_book(self):
        response = self.client.post('/api/books/', self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_book(self):
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_update_book(self):
        updated_data = self.book_data.copy()
        updated_data['title'] = 'Updated Test Book'
        response = self.client.put(f'/api/books/{self.book.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Test Book')

    def test_delete_book(self):
        response = self.client.delete(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

class LibraryUserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
        self.library_user = LibraryUser.objects.create(user=self.user)

    def test_create_library_user(self):
        user_data = {
            'username': 'newuser',
            'password': 'newpass',
            'email': 'newuser@example.com'
        }
        user = User.objects.create_user(**user_data)
        library_user_data = {
            'user': user.id,
            'active_status': True
        }
        response = self.client.post('/api/users/', library_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_library_user(self):
        response = self.client.get(f'/api/users/{self.library_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], self.user.username)

    def test_update_library_user(self):
        updated_data = {
            'user': self.user.id,
            'active_status': False
        }
        response = self.client.put(f'/api/users/{self.library_user.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.library_user.refresh_from_db()
        self.assertFalse(self.library_user.active_status)

    def test_delete_library_user(self):
        response = self.client.delete(f'/api/users/{self.library_user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(LibraryUser.objects.filter(id=self.library_user.id).exists())

class BorrowedBookTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
        self.library_user = LibraryUser.objects.create(user=self.user)
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            isbn='1234567890123',
            published_date='2023-01-01',
            number_of_copies_available=5
        )

    def test_check_out_book(self):
        borrowed_book_data = {
            'user': self.library_user.id,
            'book': self.book.id
        }
        response = self.client.post('/api/borrowed-books/', borrowed_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.book.refresh_from_db()
        self.assertEqual(self.book.number_of_copies_available, 4)

    def test_return_book(self):
        borrowed_book = BorrowedBook.objects.create(user=self.library_user, book=self.book)
        return_data = {
            'returned_date': '2023-01-02'
        }
        response = self.client.put(f'/api/borrowed-books/{borrowed_book.id}/', return_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.number_of_copies_available, 5)
        borrowed_book.refresh_from_db()
        self.assertIsNotNone(borrowed_book.returned_date)
