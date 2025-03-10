from django.test import TestCase, client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import PostModel, ProfileModel


class TestViews(TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)

    def setUp(self):
        print("setUp")
        self.client = client.Client()
        self.User = User.objects.create_user(username = 'testuser', email = 'test@gmail.com',
                                             password='<testpassword>', is_active = True, is_staff = True)
        self.post = PostModel(author = self.User, text = 'test post')

    def test_feed_view(self):
        print('test_feed_view')
        self.client.force_login(user = self.User)
        response = self.client.get(reverse('feed'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/feed.html')
        self.assertContains(response, '<title>Feed</title>')
        self.assertIn('posts', response.context)

    def test_profile_view(self):
        print('test_profile_view')
        ProfileModel.objects.filter(user = self.User).update(bio = 'test bio')

        self.client.force_login(user = self.User)
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/profile.html')
        self.assertContains(response, '<title>Profile</title>')
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'test bio')
        self.assertIn('posts', response.context)
        self.assertIn('user', response.context)
        self.assertEqual(response.context['user'], self.User)

    def test_posting_view(self):
        self.client.login(username = 'testuser', password = '<testpassword>')
        response = self.client.get(reverse('post'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/new_post.html')
        self.assertContains(response, '<title>New post</title>')
        self.assertIn('form', response.context)
        self.assertIn('formset', response.context)

    def test_automatic_profile_creation(self):
        print('test_automatic_profile_creation')
        self.client.login(username = 'testuser', password = '<testpassword>')
        self.assertEqual(ProfileModel.objects.count(), 1)

    def test_profile_edit_view(self):
        print('test_profile_edit_view')
        self.client.force_login(user = self.User)
        response = self.client.get(reverse('edit_profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/edit_profile.html')

        response = self.client.post(reverse('edit_profile'), {
            'first_name': 'test',
            'last_name': 'test',
            'gender': 'male',
            'avatar': 'avatars/default_avatar.png',
            'birth_date': '2000-01-01',
            'bio': 'test bio'
        })

        self.assertEqual(response.status_code, 302)

        profile = ProfileModel.objects.get(user = self.User)

        self.assertEqual(profile.first_name, 'test')
        self.assertEqual(profile.last_name, 'test')
        self.assertEqual(profile.gender, 'male')
        self.assertEqual(profile.avatar, 'avatars/default_avatar.png')
        self.assertEqual(profile.birth_date.strftime('%Y-%m-%d'), '2000-01-01')
        self.assertEqual(profile.bio, 'test bio')

    def test_redirect_to_login_when_not_authenticated(self):
        print('test_redirect_to_login_when_not_authenticated')
        response = self.client.get(reverse('feed'))
        self.assertEqual(response.url, '/login?next=/feed')

        response = self.client.get(reverse('edit_profile'))
        self.assertEqual(response.url, '/login?next=/profile/edit')

        response = self.client.get(reverse('profile'))
        self.assertEqual(response.url, '/login?next=/profile/')

        response = self.client.get(reverse('post')) #get method
        self.assertEqual(response.url, '/login?next=/post')

        response = self.client.post(reverse('post')) #post method
        self.assertEqual(response.url, '/login?next=/post')

    def test_login_view(self):
        print('test_login_view')
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/login.html')
        self.assertContains(response, '<title>Login</title>')
        self.assertIn('form', response.context)

        response = self.client.post(reverse('login') + '?next=/feed',
                                    {'username' : 'testuser', 'password' : '<testpassword>'})
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/feed')

    def test_register_view(self):
        print('test_register_view')
        response = self.client.get(reverse('register'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/registration.html')
        self.assertContains(response, '<title>Registration</title>')
        self.assertIn('form', response.context)

        response = self.client.post(reverse('register'), {
            'username': 'testuser2',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
            'email': 'test@gmail.com',
        })

        new_user = User.objects.filter(username = 'testuser2').first()

        self.assertEqual(new_user.username, 'testuser2')
        self.assertEqual(new_user.email, 'test@gmail.com')
        self.assertEqual(new_user.is_active, False)

    def test_activate_account_view(self):
        print('test_activate_account_view')
        response = self.client.get(reverse('activate_account', args = ('testuid', 'testtoken')))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'myapp/activation.html')
        self.assertContains(response, '<title>Account activation</title>')
        self.assertIn('message', response.context)
