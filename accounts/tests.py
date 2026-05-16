from django.urls import reverse
from django.test import Client, TestCase

from accounts.models import CustomUser
from blog.models import Post


class AccountFlowTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_creates_new_user_and_redirects_to_login(self):
        response = self.client.post(
            reverse('accounts:register'),
            {
                'email': 'newuser@example.com',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
        )
        assert response.status_code == 302
        assert reverse('accounts:login') in response.url
        assert CustomUser.objects.filter(email='newuser@example.com').exists()

    def test_new_user_can_login_after_registration(self):
        self.client.post(
            reverse('accounts:register'),
            {
                'email': 'newuser2@example.com',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
        )
        login_response = self.client.post(
            reverse('accounts:login'),
            {'username': 'newuser2@example.com', 'password': 'StrongPass123!'},
        )
        assert login_response.status_code == 302
        assert login_response.url == reverse('blog:post_list')

    def test_logout_redirects_to_blog_home(self):
        user = CustomUser.objects.create_user(email='logoutuser@example.com', password='LogoutPass123!')
        self.client.force_login(user)
        response = self.client.get(reverse('accounts:logout'))
        assert response.status_code == 302
        assert response.url == reverse('blog:post_list')

    def test_logged_out_user_sees_like_prompt_on_post_detail(self):
        user = CustomUser.objects.create_user(email='logoutuser2@example.com', password='LogoutPass123!')
        post = Post.objects.create(
            title='Public post',
            slug='public-post',
            content='Public content',
            author=user,
            is_published=True,
        )
        self.client.force_login(user)
        self.client.get(reverse('accounts:logout'))
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': post.slug}))
        assert response.status_code == 200
        assert b'Login to like' in response.content
