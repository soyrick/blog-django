import pytest
from django.urls import reverse

from blog.models import Post


def test_reader_can_view_published_post(client, user_reader, post):
    client.force_login(user_reader)
    response = client.get(reverse('blog:post_detail', kwargs={'slug': post.slug}))
    assert response.status_code == 200
    assert b'Test Post' in response.content


def test_author_can_edit_own_post(client, user_author, post):
    client.force_login(user_author)
    response = client.get(reverse('blog:post_update', kwargs={'slug': post.slug}))
    assert response.status_code == 200


def test_reader_cannot_edit_other_post(client, user_reader, post):
    client.force_login(user_reader)
    response = client.get(reverse('blog:post_update', kwargs={'slug': post.slug}))
    assert response.status_code in (302, 403)


def test_moderator_can_delete_any_post(client, user_moderator, post):
    client.force_login(user_moderator)
    response = client.post(reverse('blog:post_delete', kwargs={'slug': post.slug}))
    assert response.status_code == 302
    assert not Post.objects.filter(pk=post.pk).exists()


def test_htmx_like_endpoint_returns_fragment(client, user_reader, post):
    client.force_login(user_reader)
    response = client.post(
        reverse('blog:post_like', kwargs={'slug': post.slug}),
        HTTP_HX_REQUEST='true'
    )
    assert response.status_code == 200
    assert b'<button' in response.content
    assert b'1' in response.content
