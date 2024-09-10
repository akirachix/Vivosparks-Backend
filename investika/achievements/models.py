from django.db import models
from django.conf import settings



def get_default_user_id(apps, schema_editor):
    User = apps.get_model('users', 'User')
    default_user = User.objects.first()  
    return default_user.id

class Achievement(models.Model):
    
    """
    The Achievement class represents an accomplishment that a user can earn. 
    It includes details about the achievement, such as its title, description, 
    criteria, and the type of reward given. The class also links to a specific 
    user and tracks when the achievement was created. It is designed to support
    various reward types and integrates with Django's user management system.
    """
    
    REWARD_TYPE_CHOICES = [
        ('Badge', 'Badge'),
        ('Extra Virtual Money', 'Extra Virtual Money'),
    ]

    id = models.CharField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,default=None)
    criteria = models.TextField()
    date_achieved = models.DateField()
    description = models.TextField()
    reward_type = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True) 

    def soft_delete(self):
        self.is_active = False
        self.save() 

    def __str__(self):
        return f"Achievement {self.title}"
