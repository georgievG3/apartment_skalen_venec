from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Чака плащане'),
        ('paid', 'Платено'),
        ('cancelled', 'Отменено'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations'
    )

    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    people = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"