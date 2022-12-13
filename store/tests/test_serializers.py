from unittest import TestCase

from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BookSerializersTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='pa211efedf22w22', first_name='Ivan',
                                    last_name='Petrov')
        user2 = User.objects.create(username='pa21efedf2122w22', first_name='Ivan',
                                    last_name='Sidorov')
        user3 = User.objects.create(username='pa13efdef21w2222', first_name='1',
                                    last_name='2')

        book_1 = Book.objects.create(name='Test book 1', price=100,
                                     author_name='Author 1', owner=user1)
        book_2 = Book.objects.create(name='Test book 2', price=100,
                                     author_name='Author 2')
        UserBookRelation.objects.create(user=user1, book=book_1, like=True,
                                        rate=2)
        UserBookRelation.objects.create(user=user2, book=book_1, like=True,
                                        rate=2)
        UserBookRelation.objects.create(user=user3, book=book_1, like=True,
                                        rate=2)

        UserBookRelation.objects.create(user=user1, book=book_2, like=True,
                                        rate=3)
        UserBookRelation.objects.create(user=user2, book=book_2, like=True,
                                        rate=3)
        UserBookRelation.objects.create(user=user3, book=book_2, like=False,
                                        rate=3)

        books = Book.objects.filter(id__in=[book_1.id, book_2.id]).annotate(
            annotated_likes=Count(
                Case(When(userbookrelation__like=True, then=1))))
        data = BooksSerializer(books, many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '100.00',
                'author_name': 'Author 1',

                'annotated_likes': 3,
                'rating': '2.00',
                'owner_name': 'user1',
                'readers': [
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Petrov'
                    },
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Sidorov'
                    },
                    {
                        'first_name': 1,
                        'last_name': 2
                    }
                ]
            },
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '100.00',
                'author_name': 'Author 2',

                'annotated_likes': 2,
                'rating': '3.00',
                'owner_name': '',
                'readers': [
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Petrov'
                    },
                    {
                        'first_name': 'Ivan',
                        'last_name': 'Sidorov'
                    },
                    {
                        'first_name': 1,
                        'last_name': 2
                    }
                ]
            },
        ]
        self.assertEqual(expected_data, data)
