"""

The **jumpstart.tests.py** file provides error handling mechanisms for Test Cases in the project

"""

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase



class LoginTests(TestCase):
    def setUp(self):
        User.objects.create(username="test1", password="test1")
        User.objects.create(username="test2", password="test2")

    def test_no_user_input_login(self):
        """Should not allow a user to login if no account exists

        """
        temp = True
        user = None
        try:
            user = User.objects.get(username="", password="")
        except User.DoesNotExist:
            pass

        self.assertEqual(user, None)

    def test_duplicate_account(self):
        """Should not allow duplicate accounts with same credentials

        """
        user = None
        try:
            user = User.objects.filter(username="test1")
        except User.DoesNotExist:
            pass

        users = user.count()
        self.assertEqual(users, 1)