from django.test import TestCase, client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import PostModel, Profile

class TestViews(TestCase):
    def setUp(self):
        self.client = client.Client()
        self.User = User.objects.create_user(username = 'testuser', password = '<testpassword>',
                                                         email = 'test@gmail.com', is_active = True, is_staff = True)
        self.profile = Profile.objects.create(user = self.User, bio = 'test bio')
        self.post = PostModel.objects.create(author = self.User, text = 'test post')
        print(self.post)

    def test_feed_view(self):
        self.client.login(username = 'testuser', password = '<testpassword>')
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/feed.html')
        self.assertContains(response, '<title>Feed</title>')
        self.assertIn('posts', response.context)

    def test_profile_view(self):
        self.client.login(username = 'testuser', password = '<testpassword>')
        # self.profile = ProfileModel.objects.create(user = self.User, bio = 'test bio')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/profile.html')
        self.assertContains(response, '<title>Profile</title>')
        # self.assertContains(response, 'testuser')
        self.assertContains(response, 'test bio')
        self.assertIn('posts', response.context)
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], self.User)

    def posting_view(self):
        self.client.login(username = 'testuser', password = '<testpassword>')
        response = self.client.get(reverse('post'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/new_post.html')
        self.assertContains(response, '<title>New Post</title>')
        self.assertIn('form', response.context)
        self.assertIn('formset', response.context)

    # def automatic_profile_creation(self):
    #     self.client.login(username = 'testuser', password = '<testpassword>')
    #     self.assertEqual(Profile.objects.count(), 1)
