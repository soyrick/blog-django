import pytest
from django.contrib.auth.models import Group
from django.test import Client
from accounts.models import CustomUser
from blog.models import Post


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user_admin(db):
    return CustomUser.objects.create_superuser(email='admin@example.com', password='password123')


@pytest.fixture
def user_moderator(db):
    moderator = CustomUser.objects.create_user(email='moderator@example.com', password='password123')
    Group.objects.get_or_create(name='Moderator')
    moderator.groups.add(Group.objects.get(name='Moderator'))
    return moderator


@pytest.fixture
def user_author(db):
    author = CustomUser.objects.create_user(email='author@example.com', password='password123')
    Group.objects.get_or_create(name='Author')
    author.groups.add(Group.objects.get(name='Author'))
    return author


@pytest.fixture
def user_reader(db):
    reader = CustomUser.objects.create_user(email='reader@example.com', password='password123')
    Group.objects.get_or_create(name='Reader')
    reader.groups.add(Group.objects.get(name='Reader'))
    return reader


@pytest.fixture
def post(db, user_author):
    return Post.objects.create(
        title='Test Post',
        slug='test-post',
        content='This is a test post.',
        author=user_author,
        is_published=True,
    )
