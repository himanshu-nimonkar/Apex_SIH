from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class GraphicalPassword(models.Model):
    """
    Stores the graphical password for each user.
    The image_sequence is stored as a hashed value for security.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='graphical_password')
    image_sequence_hash = models.CharField(max_length=128)  # Hashed sequence
    salt = models.CharField(max_length=32)  # Salt for hashing
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Graphical Password for {self.user.username}"
