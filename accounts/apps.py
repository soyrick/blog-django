from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        def create_roles(sender, **kwargs):
            from django.contrib.auth.models import Group

            for group_name in ['Moderator', 'Author', 'Reader']:
                Group.objects.get_or_create(name=group_name)

        post_migrate.connect(create_roles, sender=self)
