from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import EmailValidator, MinLengthValidator
from django.db import models

from accounts.managers import AppUserManager


# Create your models here.
class AppUser(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'

    email = models.EmailField(unique=True, validators=[EmailValidator()])
    first_name = models.CharField(max_length=30, validators=[MinLengthValidator(3,message="Името трябва да е поне 3 символа.")])
    last_name = models.CharField(max_length=30, validators=[MinLengthValidator(3, message="Името трябва да е поне 3 символа.")])
    is_staff = models.BooleanField(default=False,)
    is_active = models.BooleanField(default=True,)

    objects = AppUserManager()


class Profile(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, validators=[MinLengthValidator(9)])
    nationality = models.CharField(max_length=20, validators=[MinLengthValidator(3)])

    def is_complete(self):
        required_fields = [self.phone_number, self.date_of_birth]
        return all(required_fields)