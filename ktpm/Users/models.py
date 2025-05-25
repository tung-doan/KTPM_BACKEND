# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('manager', 'Tổ trưởng'),
        ('deputy', 'Tổ phó'),
        ('accountant', 'Kế toán'),
    )
    
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    unit_code = models.CharField(max_length=50, null=True, blank=True)
    manager = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to={'role': 'manager'},
        related_name='subordinates'
    )

    def __str__(self):
        return self.username

    class Meta:
        indexes = [
            models.Index(fields=['unit_code']),
        ]