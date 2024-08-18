#user_authorization/froms.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=False, default="Unknown address")
    groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True, related_name='custom_user_permissions')
    house_number = models.CharField(max_length=10, blank=False, default="0")
    city = models.CharField(max_length=100, blank=False, default="Unknown city")
    postal_code = models.CharField(max_length=10, blank=False, default="00000")

    def __str__(self):
        return self.username


