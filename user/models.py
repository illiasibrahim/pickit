from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models.expressions import F
from django.db.models.fields import EmailField

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,phone,email,username,password=None):
        if not phone:
            raise ValueError('User must have a phone number')
        if not email:
            raise ValueError('User must have a email address')

        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            phone = phone,
            username = username,
            
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, phone, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            username = username,
            phone = phone,
            first_name = first_name,
            last_name = last_name,

        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.has_access = True

        user.save(using = self._db)
        return user


class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    email           = models.EmailField(max_length=100, unique=True)
    username        = models.CharField(max_length=50, blank=True)
    phone           = models.CharField(max_length=13, unique=True)

    #required

    has_access      = models.BooleanField(default=True)
    data_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=True)
    is_staff        = models.BooleanField(default=False)
    is_superadmin   = models.BooleanField(default=False)

    USERNAME_FIELD  = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email','username']

    objects = MyAccountManager()


    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
