from django.test import TestCase, client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import PostModel

class TestViews(TestCase):
    def setUp(self):
        self.client = client.Client()
        self.user = self.User = User.objects.create_user(username = 'testuser', passwords = '<testpassword>',
                                                         email = 'test@gmail.com', is_active = True, is_staff = True)

    def