from django.db import models
from django.contrib.auth.models import User
from django.db import models


class Property(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    area_sqft = models.FloatField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    




class UserSearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional if anonymous users
    query = models.TextField()
    city = models.CharField(max_length=100, null=True, blank=True)
    budget = models.IntegerField(null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.query} ({self.timestamp})"
    



class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey('Property', on_delete=models.CASCADE)
    visit_date = models.DateField()
    visit_time = models.TimeField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed')], default='Pending')

    def __str__(self):
        return f"Booking: {self.user.username} -> {self.property.title} on {self.visit_date} at {self.visit_time}"


