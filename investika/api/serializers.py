from rest_framework import serializers
from users.models import User


class UserSerialzer(serializers.ModelSerializer):
     password =serializers.CharField(write_only= True, required= True)
     class Meta:
         model=User
         fields=['email','username','password']
     def create (self,validates_data):
         password= validates_data.pop('password',None)
         user =User(**validates_data)
         if password:
             user.set_password(password)
             user.save()
             return user
        