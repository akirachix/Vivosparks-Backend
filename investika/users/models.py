from django.db import models


"""
This model defines the structure for the `User` table in the database.
It includes fields for storing the user's information such as username, email, password, age, gender, location, income, and avatar URL.
The model also automatically records when the user is created with the `created_at` field.
The `user_id` field is the primary key, and the `__str__` method returns the username for better readability in Django admin and print statements.

"""

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

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
    )
    location = models.CharField(max_length=100)
    income = models.DecimalField(max_digits=10, decimal_places=2)

    avatar = models.CharField(
        max_length=50,
        choices=AVATAR_CHOICES,
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def soft_delete(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return self.username
