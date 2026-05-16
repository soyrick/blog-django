from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction

from blog.models import Comment, Like, Post


class Command(BaseCommand):
    help = 'Seed the blog with sample users, posts, comments, and likes.'

    def handle(self, *args, **options):
        User = get_user_model()

        with transaction.atomic():
            Group.objects.get_or_create(name='Moderator')
            Group.objects.get_or_create(name='Author')
            Group.objects.get_or_create(name='Reader')

            author, _ = User.objects.get_or_create(
                email='author@blog.test',
                defaults={'is_active': True}
            )
            if not author.has_usable_password():
                author.set_password('Author123!')
                author.save()
            reader, _ = User.objects.get_or_create(
                email='reader@blog.test',
                defaults={'is_active': True}
            )
            if not reader.has_usable_password():
                reader.set_password('Reader123!')
                reader.save()
            moderator, _ = User.objects.get_or_create(
                email='moderator@blog.test',
                defaults={'is_active': True}
            )
            if not moderator.has_usable_password():
                moderator.set_password('Moderator123!')
                moderator.save()
            admin, _ = User.objects.get_or_create(
                email='admin@blog.test',
                defaults={'is_staff': True, 'is_superuser': True, 'is_active': True}
            )
            if not admin.has_usable_password():
                admin.set_password('Admin123!')
                admin.save()

            Group.objects.get(name='Author')
            author_group = Group.objects.get(name='Author')
            moderator_group = Group.objects.get(name='Moderator')
            reader_group = Group.objects.get(name='Reader')

            author.groups.add(author_group)
            moderator.groups.add(moderator_group)
            reader.groups.add(reader_group)

            sample_posts = [
                {
                    'title': 'Cómo empezamos en la comunidad',
                    'slug': 'como-empezamos-en-la-comunidad',
                    'content': 'Bienvenido al blog comunitario. Aquí puedes compartir ideas, comentarios y likes en un estilo moderno y oscuro.',
                    'is_published': True,
                },
                {
                    'title': 'Consejos rápidos para mejorar tu perfil',
                    'slug': 'consejos-rapidos-para-mejorar-tu-perfil',
                    'content': 'Usa un correo claro, agrega una buena foto y mantén tus publicaciones cortas y atractivas.',
                    'is_published': True,
                },
                {
                    'title': 'Este post es un borrador privado',
                    'slug': 'post-privado-borrador',
                    'content': 'Solo el autor puede ver este borrador cuando está autenticado.',
                    'is_published': False,
                },
            ]

            created_posts = []
            for data in sample_posts:
                post, created = Post.objects.update_or_create(
                    slug=data['slug'],
                    defaults={
                        'title': data['title'],
                        'content': data['content'],
                        'author': author,
                        'is_published': data['is_published'],
                    },
                )
                created_posts.append(post)

            Comment.objects.get_or_create(
                post=created_posts[0],
                author=reader,
                content='¡Genial inicio! Me encanta el diseño oscuro.',
            )
            Comment.objects.get_or_create(
                post=created_posts[1],
                author=reader,
                content='Muy buena idea compartir consejos prácticos.',
            )
            Like.objects.get_or_create(post=created_posts[0], user=reader)
            Like.objects.get_or_create(post=created_posts[1], user=reader)

            self.stdout.write(self.style.SUCCESS('Seed data installed successfully.'))
