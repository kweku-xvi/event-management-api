import uuid
from accounts.models import User
from django.utils import timezone
from django.db import models


class Event(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateField(default=timezone.now)
    time = models.TimeField()
    ticket_price = models.DecimalField(max_digits=14, decimal_places=4, default=0.00)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at',)

