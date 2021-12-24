from django.db import models

from django.contrib.auth.models import User #this is auth_user model

# Create your models here.

class note(models.Model):
    login_id=models.ForeignKey(User,on_delete=models.CASCADE)
    u_id=models.AutoField(primary_key=True)
    data=models.CharField(max_length=100)
    datetime=models.DateTimeField(auto_now_add=True)
    email=models.CharField(max_length=100,null=True)

