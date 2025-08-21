
from django.db import models
from django.utils import timezone
import random

class Candidate(models.Model):
    registration_no = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10)
    age = models.IntegerField()
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    photo = models.ImageField(upload_to='photos/')
    transaction_no = models.IntegerField(unique=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.registration_no})"
   
    # Add other fields as needed

    def save(self, *args, **kwargs):
        if not self.registration_no:
            last_id = Candidate.objects.count() + 1
            self.registration_no = f"SPQ{timezone.now().year}{last_id}"
        super().save(*args, **kwargs)

class Document(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='documents')
    document_file = models.FileField(upload_to='documents/')

    def __str__(self):
        return f"Document for {self.candidate.registration_no}"
    

class Application(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    ]

    candidate = models.OneToOneField(Candidate, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    # Optionally add fields for admin reviewer, notes, etc.

    def __str__(self):
        return f"Application for {self.candidate.registration_no} - {self.status}"
    



class PhoneOTP(models.Model):
    phone_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def is_expired(self):
        # OTP expires after 5 minutes
        return timezone.now() > self.created_at + timezone.timedelta(minutes=5)
    
    def __str__(self):
        return f"OTP for {self.phone_number}"

def generate_otp():
    return str(random.randint(100000, 999999))
