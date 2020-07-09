from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
    

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_setup = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email              = models.EmailField(verbose_name="email", max_length=60, null=True, unique=True)
    first_name         = models.CharField(max_length=30)
    last_name          = models.CharField(max_length=30)
    passworld          = models.CharField(max_length=50, blank=True, null=True)
    #autofields
    username           = None
    date_joined        = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login         = models.DateTimeField(verbose_name='last_login', auto_now=True)
    is_superuser       = models.BooleanField(default=False)
    is_admin           = models.BooleanField(default=False)
    is_staff           = models.BooleanField(default=False)
    is_active          = models.BooleanField(default=True)
    is_verified        = models.BooleanField(default=True)
    is_setup           = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def clean(self):
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True