from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class LostItem(models.Model):
    """Model for lost items posted by users"""
    
    STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
        ('claimed', 'Claimed'),
    ]
    
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('documents', 'Documents'),
        ('accessories', 'Accessories'),
        ('clothing', 'Clothing'),
        ('books', 'Books'),
        ('other', 'Other'),
    ]
    
    # Basic information
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='lost')
    
    # Location and time
    location_lost = models.CharField(max_length=200, help_text="Where was it lost/found?")
    date_lost = models.DateField(help_text="When was it lost/found?")
    
    # Image
    image = models.ImageField(upload_to='lost_items/', blank=True, null=True)
    
    # User who posted
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_items')
    contact_info = models.CharField(max_length=200, help_text="Phone or email to contact")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} - {self.status}"


class Claim(models.Model):
    """Model for claims made on lost items"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    item = models.ForeignKey(LostItem, on_delete=models.CASCADE, related_name='claims')
    claimed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='claims')
    message = models.TextField(help_text="Describe why this item is yours")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['item', 'claimed_by']  # One claim per user per item
        
    def __str__(self):
        return f"Claim by {self.claimed_by.email} on {self.item.title}"
