from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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
    def create_user(self, username, password=None, **extra_fields):
        """
        Create and return a user with a username and password.
        Email is optional.
        """
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Create and return a superuser with a username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model that uses 'username' as the unique identifier for authentication.
    """
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=False, blank=True, null=True)  # Email is now optional
    password = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='male')
    location = models.CharField(max_length=100, null=True, blank=True)
    income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    avatar = models.CharField(max_length=50, choices=AVATAR_CHOICES, default='ShadowClaw')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Manager for the User model
    objects = UserManager()

    # Use 'username' as the unique identifier for authentication
    USERNAME_FIELD = 'username'
    
    # No additional required fields
    REQUIRED_FIELDS = []  # No fields are required apart from username and password

    def __str__(self):
        return self.username
