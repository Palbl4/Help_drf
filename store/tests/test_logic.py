from unittest import TestCase

from django.contrib.auth.models import User

from store.logic import set_rating
from store.models import Book, UserBookRelation


class SetRatingTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='qed2d2e2', first_name='Ivan',
                                         last_name='Petrov')
        user2 = User.objects.create(username='qed2d22ee', first_name='Ivan',
                                         last_name='Sidorov')
        user3 = User.objects.create(username='pq2d2e2d2', first_name='1',
                                         last_name='2')

        self.book_1 = Book.objects.create(name='Test book 1', price=100,
                                          author_name='Author 1', owner=user1)
        self.book_2 = Book.objects.create(name='Test book 2', price=100,
                                          author_name='Author 2')
        UserBookRelation.objects.create(user=user1, book=self.book_1,
                                        like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=user2, book=self.book_1,
                                        like=True,
                                        rate=2)
        UserBookRelation.objects.create(user=user3, book=self.book_1,
                                        like=True,
                                        rate=3)

        UserBookRelation.objects.create(user=user1, book=self.book_2,
                                        like=True,
                                        rate=3)
        UserBookRelation.objects.create(user=user2, book=self.book_2,
                                        like=True,
                                        rate=5)
        UserBookRelation.objects.create(user=user3, book=self.book_2,
                                        like=False,
                                        rate=5)

    def test_ok(self):
        set_rating(self.book_1)
        self.book_1.refresh_from_db()
        self.assertEqual('3.33', str(self.book_1.rating))
