from django.db import models

class User(models.Model):
    # Auto-incrementing primary key field for each user
    user_id = models.AutoField(primary_key=True)
    
    # Username field to store the username with a max length of 100 characters
    username = models.CharField(max_length=100)
    
    # Email field with unique constraint to ensure each email is only used once
    email = models.EmailField(unique=True)
    
    # Password field to store the user's password (should be hashed for security purposes)
    password = models.CharField(max_length=100)
    
    # Integer field to store the user's age
    age = models.IntegerField()
    
    # Gender field with a max length of 25 characters (you might use choices here for better validation)
    gender = models.CharField(max_length=25)
    
    # Location field to store the user's location with a max length of 100 characters
    location = models.CharField(max_length=100)
    
    # Decimal field to store the user's income, allowing up to 10 digits with 2 decimal places
    income = models.DecimalField(max_digits=10, decimal_places=2)
    
    # URL field to store the avatar image URL (optional, so null and blank are allowed)
    avatar_url = models.URLField(null=True, blank=True)
    
    # Automatically adds the date and time when the user was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Method to return the username when the object is printed or viewed in Django admin
    def __str__(self):
        return self.username
