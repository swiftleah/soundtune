from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    """handles creation of custom users - email instead of username & full name
       access to BaseUserManager & its helper methods"""
    def create_user(self, email, full_name, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not full_name:
            raise ValueError("Users must provide a full name")
        
        email = self.normalize_email(email) #normalize email address
        user = self.model(email=email, full_name=full_name) #create user obj
        user.set_password(password) # hash password
        user.save(using=self._db) #save user in default db
        return user
    
    def create_superuser(self, email, full_name, password):
        #admin user
        user = self.create_user(email=email, full_name=full_name, password=password)
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
    
class CustomUser(AbstractUser, PermissionsMixin):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email' #email instead of username
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager() #set custom manager

    def __str__(self):
        return self.email
