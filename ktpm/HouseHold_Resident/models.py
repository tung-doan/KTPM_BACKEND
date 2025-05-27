from django.db import models

# Create your models here.
from django.db import models

class Household(models.Model):
    household_id = models.AutoField(primary_key=True)
    block_name = models.CharField(max_length=50)
    room_number = models.CharField(max_length=10)
    owner_name = models.CharField(max_length=100)
    number_people = models.IntegerField(default=0)
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
    id_card_number = models.CharField(max_length=20, blank=True, null=True)
    id_card_issue_date = models.DateField(blank=True, null=True)
    id_card_issue_place = models.CharField(max_length=100, blank=True, null=True)
    # tam tru tam vang sinh song
    status = models.CharField(
        max_length=20,
        choices=[
            ('sinh_song', 'Sinh sống'),
            ('tam_vang', 'Tạm vắng'),
            ('tam_tru', 'Tạm trú')
        ],
        default='sinh_song'
    )
    def __str__(self):
        return self.full_name