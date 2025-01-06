from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        if phone_number:
            if CustomUser.objects.filter(phone_number=phone_number).exists():
                raise ValidationError(f"The phone number {phone_number} is already in use.")
        else:
            phone_number = None  # handle blank
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, phone_number, password, **extra_fields)


class CustomUser(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True,
                                    validators=[
                                        RegexValidator(
                                            regex=r'^(\+254|0)([7][0-9]|[1][0-1]){1}[0-9]{1}[0-9]{6}$',
                                            message="Phone number must start with +254 or 0 and be followed by valid digits."
                                        )],
                                    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
