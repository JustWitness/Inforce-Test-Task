from django.db import models
from django.contrib.auth.models import AbstractUser
from .enums import UserRole


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=UserRole,
        default=UserRole.EMPLOYEE
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    def __str__(self) -> str:
        return f"{self.email} {self.role}"
