from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# Choices for gender and avatar
GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
]

AVATAR_CHOICES = [
    ('ShadowClaw', 'ShadowClaw'),
    ('Thunderwing', 'Thunderwing'),
    ('MysticFlare', 'MysticFlare'),
    ('AuroraBreath', 'AuroraBreath'),
]

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)  # Allow age to be null (optional)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='male')  # Provide default for gender
    location = models.CharField(max_length=100, null=True, blank=True)  # Optional field for location
    income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Optional field for income
    avatar = models.CharField(max_length=50, choices=AVATAR_CHOICES, default='ShadowClaw')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def soft_delete(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.username
