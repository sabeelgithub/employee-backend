# Create your models here.
from django.contrib.auth.models import AbstractUser,PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid



class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, username,email,phone, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(username=username,email=email,phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username,email,phone, password=None, **extra_fields):
        return self._create_user(username,email,phone,password, **extra_fields)

    def create_superuser(self,username, email,phone, password=None,is_superuser=True,is_staff=True, **extra_fields):
        return self._create_user(username,email, phone,password,is_superuser=is_superuser,is_staff=is_staff, **extra_fields)
        
class CustomUser(AbstractUser,PermissionsMixin):
    first_name = None
    last_name = None
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=244,unique=True)
    email = models.EmailField(_('email address'),unique=True,null=True,blank=True)
    phone = models.BigIntegerField(unique=True,null=True,blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone','email']

    objects = CustomUserManager()

    def __str__(self):  
        return f'{self.username}' 
    