import pytest
from django.db import IntegrityError

from blog.models import Comment, Like, Post


def test_post_str(post):
    assert str(post) == 'Test Post'


def test_comment_creation(db, user_author, post):
    comment = Comment.objects.create(post=post, author=user_author, content='Nice post')
    assert comment.post == post
    assert 'Comment by' in str(comment)


def test_like_unique_constraint(db, user_reader, post):
    Like.objects.create(post=post, user=user_reader)
    with pytest.raises(IntegrityError):
        Like.objects.create(post=post, user=user_reader)
