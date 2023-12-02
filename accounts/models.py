import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self,email,password:None,**extra_fields):
        if not email:
            raise ValueError(_("The email is Required"))
        email = self.normalize_email(email=email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("SuperUser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("SuperUser must have is_superuser=True"))
        
        return self.create_user(email,password,**extra_fields)


class User(AbstractUser):
    id = models.CharField(primary_key=True, unique=True, max_length=8)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    phone_number = models.CharField(unique=True, max_length=15)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'date_of_birth']

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    
