from django.db import models

# Create your models here.
from django.db import models

class Household(models.Model):
    household_id = models.AutoField(primary_key=True)
    block_name = models.CharField(max_length=50)
    room_number = models.CharField(max_length=10)
    owner_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.block_name} - {self.room_number} ({self.owner_name})"

class Citizen(models.Model):
    citizen_id = models.AutoField(primary_key=True)
    household = models.ForeignKey(
        Household,
        on_delete=models.CASCADE,
        db_column='household_id'
    )
    full_name = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Nam'), ('female', 'Nữ')],
        blank=True,
        null=True
    )
    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=100, blank=True, null=True)
    origin_place = models.CharField(max_length=100, blank=True, null=True)
    job = models.CharField(max_length=100, blank=True, null=True)
    workplace = models.CharField(max_length=100, blank=True, null=True)
    id_card_number = models.CharField(max_length=20, blank=True, null=True)
    id_card_issue_date = models.DateField(blank=True, null=True)
    id_card_issue_place = models.CharField(max_length=100, blank=True, null=True)
    previous_residence = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.full_name