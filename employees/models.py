from django.db import models
# from django.contrib.auth.models import User
import uuid

from accounts.models import CustomUser

class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=100)
    custom_fields = models.JSONField()  # Custom fields storage
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.name