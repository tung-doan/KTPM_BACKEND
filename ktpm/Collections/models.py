from django.db import models
from Users.models import User

class Collection(models.Model):
    collection_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=11, unique=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    amount = models.PositiveIntegerField()
    unit_code = models.CharField(max_length=50)
    recorded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'role': 'accountant'}
    )

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['unit_code']),
        ]
