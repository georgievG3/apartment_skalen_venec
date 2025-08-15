from django.db import models

# Create your models here.
class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Чака плащане'),
        ('paid', 'Платено'),
        ('cancelled', 'Отменено'),
    ]

    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.start_date} - {self.end_date})"