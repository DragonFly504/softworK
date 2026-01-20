from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Extended user profile with additional fields"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Personal Information
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    ssn = models.CharField(max_length=11, blank=True, null=True)  # Format: XXX-XX-XXXX
    
    # Address Information
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, default='US', blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"{self.user.email} - Profile"
    
    def get_full_address(self):
        """Return formatted full address"""
        parts = [self.address, self.city, self.state, self.zipcode, self.country]
        return ', '.join(filter(None, parts))
    
    def get_masked_ssn(self):
        """Return masked SSN (XXX-XX-1234)"""
        if self.ssn and len(self.ssn) >= 4:
            return f"XXX-XX-{self.ssn[-4:]}"
        return None
