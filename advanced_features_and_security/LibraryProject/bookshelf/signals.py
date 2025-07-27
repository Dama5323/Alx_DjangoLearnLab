# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from .models import CustomUser
from django.contrib.contenttypes.models import ContentType
from .models import Book

@receiver(post_save, sender=CustomUser)
def assign_role_permissions(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'librarian':
            content_type = ContentType.objects.get_for_model(Book)
            permissions = Permission.objects.filter(content_type=content_type)

            for perm in permissions:
                instance.user_permissions.add(perm)
        elif instance.role == 'student':
            # Example: students can only view books
            content_type = ContentType.objects.get_for_model(Book)
            view_permission = Permission.objects.get(
                codename='can_view', content_type=content_type)
            instance.user_permissions.add(view_permission)
