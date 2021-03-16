from django.test import TestCase
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType


class TestCaseBackend(TestCase):
    def add_permission(self, user, object, perm):
        content_type = ContentType.objects.get_for_model(object)
        permission = Permission.objects.get(
            content_type=content_type,
            codename=perm,
        )
        user.user_permissions.add(permission)

    def add_user(self, username, password):
        """create a user and store it under self.user_{username}"""
        user = User.objects.create_user(
            username=username,
            password=password,
        )
        setattr(self, f"user_{username}", user)
