from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not date_of_birth:
            raise ValueError("Date of birth is required")
        email = self.normalize_email(email)
        user = self.model(email=email, date_of_birth=date_of_birth, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, date_of_birth, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('customer', 'Customer'),
    )

    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')
    shipping_address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def is_of_age(self):
        return (timezone.now().date() - self.date_of_birth).days >= 6570
