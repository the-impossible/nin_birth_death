from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.shortcuts import reverse
import uuid
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# My app imports

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email=None, nin=None, password=None):

        # creates a user with the parameters
        if not email and not nin:
            raise ValueError('NIN or Email address is required!')

        if password is None:
            raise ValueError('Password is required!')

        if nin and email:
            user = self.model(
                email=self.normalize_email(email),
                nin=nin.upper().strip(),
            )

        elif nin is not None:
            user = self.model(
                nin=nin.upper().strip(),
            )

        elif email is not None:
            user = self.model(
                email=self.normalize_email(email),
            )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        # create a superuser with the above parameters
        if not email:
            raise ValueError('Email Address is required!')

        if password is None:
            raise ValueError('Password should not be empty')

        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    cert_no = models.CharField(
        max_length=10, db_index=True, unique=True, blank=True, null=True)
    nin = models.CharField(
        max_length=10, db_index=True, unique=True, blank=True, null=True)
    email = models.CharField(max_length=100, db_index=True, unique=True,
                             verbose_name='email address', blank=True, null=True)
    pic = models.ImageField(null=True, blank=True,
                            upload_to='uploads/', default='img/user.png')

    date_joined = models.DateTimeField(
        verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(
        verbose_name='last_login', auto_now=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    # REQUIRED_FIELDS = ['email',]

    objects = UserManager()

    def __str__(self):
        if self.is_hospital or self.is_staff:
            return f'{self.email}'
        else:
            if self.email:
                return f'{self.email}'

            return f'{self.nin}'

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return reverse("reg:account_profile", kwargs={
            'pk': self.user_id
        })

    def clean(self):
        if self.email != None:
            try:
                validate_email(self.email)
            except ValidationError as e:
                raise ValidationError('Invalid Email!')

    class Meta:
        db_table = 'Users'
        verbose_name_plural = 'Users'
