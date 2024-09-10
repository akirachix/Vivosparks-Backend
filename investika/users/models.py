from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

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
    """
    Custom manager for the User model.

    Provides methods to create regular users and superusers.
    """

    def create_user(self, email, username, password=None, **extra_fields):
        """
        Create and return a regular user with an email, username, and password.

        Args:
            email (str): The user's email address.
            username (str): The user's username.
            password (str, optional): The user's password.
            **extra_fields: Any additional fields to set on the user.

        Returns:
            User: The created user instance.
        
        Raises:
            ValueError: If the email is not provided.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Create and return a superuser with an email, username, and password.

        Args:
            email (str): The user's email address.
            username (str): The user's username.
            password (str, optional): The user's password.
            **extra_fields: Any additional fields to set on the superuser.

        Returns:
            User: The created superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model.

    This model extends the default Django user model by adding additional fields such as age, gender,
    location, income, and avatar. It also uses email as the unique identifier for authentication.
    """

    # user_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key for the user.
    # username = models.CharField(max_length=100, unique=True)  # Unique username for the user.
    # email = models.EmailField(unique=True)  # Unique email address for the user.
    # age = models.IntegerField(null=True, blank=True)  # Optional field to store the user's age.
    # gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='male')  # Gender selection for the user.
    # location = models.CharField(max_length=100, null=True, blank=True)  # Optional field to store the user's location.
    # income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Optional field for user's income.
    # avatar = models.CharField(max_length=50, choices=AVATAR_CHOICES, default='ShadowClaw')  # Avatar selection for the user.
    # created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the user was created.
    # is_active = models.BooleanField(default=True)  # Indicates whether the user account is active.
    # is_staff = models.BooleanField(default=False)  # Indicates whether the user can log into the admin site.

    user_id = models.AutoField(primary_key=True)  # Auto-incrementing primary key for the user.
    username = models.CharField(max_length=100, unique=True)  # Unique username for the user.
    email = models.EmailField(unique=True)  # Unique email address for the user.
    password = models.CharField(max_length=128)  # Storing hashed password (length 128 is typical for Django).
    age = models.IntegerField(null=True, blank=True)  # Optional field to store the user's age.
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='male')  # Gender selection for the user.
    location = models.CharField(max_length=100, null=True, blank=True)  # Optional field to store the user's location.
    income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Optional field for user's income.
    avatar = models.CharField(max_length=50, choices=AVATAR_CHOICES, default='ShadowClaw')  # Avatar selection for the user.
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the user was created.
    is_active = models.BooleanField(default=True)  # Indicates whether the user account is active.
    is_staff = models.BooleanField(default=False)  # Indicates whether the user can log into the admin site.

    def __str__(self):
        return self.username


    objects = UserManager()  # Use the custom UserManager to manage users.

    USERNAME_FIELD = 'email'  # Use email as the unique identifier for authentication.
    REQUIRED_FIELDS = ['username']  # Fields that are required when creating a user.

    def __str__(self):
        """
        Return a string representation of the user.

        Returns:
            str: The username of the user.
        """
        return self.username
