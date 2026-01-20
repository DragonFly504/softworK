from django.db import models
from django.conf import settings
from django.utils import timezone


class Shipment(models.Model):
    STATUS_CHOICES = [
        ("created", "Created"),
        ("in_transit", "In Transit"),
        ("out_for_delivery", "Out for Delivery"),
        ("delivered", "Delivered"),
        ("failed", "Delivery Failed"),
    ]

    tracking_number = models.CharField(max_length=32, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="created")

    # Sender Info
    sender_name = models.CharField(max_length=255, blank=True, default="Smith Industries")
    sender_email = models.EmailField(blank=True)
    sender_phone = models.CharField(max_length=20, blank=True)

    # Receiver Info
    receiver_name = models.CharField(max_length=255, blank=True, default="Johnson & Co.")
    receiver_email = models.EmailField(blank=True)
    receiver_phone = models.CharField(max_length=20, blank=True)

    # Package Info
    package_description = models.CharField(max_length=255, blank=True, default="Electronic Components & Parts")
    weight = models.FloatField(null=True, blank=True)
    dimensions = models.CharField(max_length=255, blank=True)

    # Locations
    origin = models.CharField(max_length=255, blank=True)
    destination = models.CharField(max_length=255, blank=True)

    origin_lat = models.FloatField(null=True, blank=True)
    origin_lng = models.FloatField(null=True, blank=True)
    dest_lat = models.FloatField(null=True, blank=True)
    dest_lng = models.FloatField(null=True, blank=True)

    current_lat = models.FloatField(null=True, blank=True)
    current_lng = models.FloatField(null=True, blank=True)
    current_location = models.CharField(max_length=255, blank=True)

    estimated_delivery = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['tracking_number']),  # Speed up tracking lookups
            models.Index(fields=['status']),  # Speed up status filters
            models.Index(fields=['created_at']),  # Speed up date filters
        ]

    def __str__(self):
        return f"Shipment {self.tracking_number} ({self.status})"

    def is_delivered(self):
        return self.status == "delivered"

    def progress_percentage(self):
        """Calculate progress based on status."""
        status_order = ["created", "in_transit", "out_for_delivery", "delivered"]
        try:
            return (status_order.index(self.status) + 1) / len(status_order) * 100
        except ValueError:
            return 0

    def to_dict(self):
        """Convert shipment to dictionary for API response."""
        return {
            'tracking_number': self.tracking_number,
            'status': self.status,
            'progress': int(self.progress_percentage()),
            'origin': self.origin,
            'destination': self.destination,
            'weight': self.weight,
            'sender_name': self.sender_name,
            'receiver_name': self.receiver_name,
            'receiver_phone': self.receiver_phone,
            'package_description': self.package_description,
            'est_delivery': self.estimated_delivery.strftime('%m/%d/%Y') if self.estimated_delivery else 'N/A',
            'current_lat': self.current_lat,
            'current_lng': self.current_lng,
            'current_location': self.current_location or self.origin,
            'created_at': self.created_at.strftime('%m/%d/%Y %H:%M'),
            'events': [event.to_dict() for event in self.events.all()]
        }


class ShipmentEvent(models.Model):
    shipment = models.ForeignKey(Shipment, related_name="events", on_delete=models.CASCADE)
    status = models.CharField(max_length=64)
    location = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.status} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    def to_dict(self):
        """Convert event to dictionary for API response."""
        return {
            'status': self.status,
            'location': self.location,
            'timestamp': self.timestamp.strftime('%m/%d/%Y %H:%M'),
            'description': self.notes,
        }
