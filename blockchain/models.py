import hashlib
import json

from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from PIL import Image



class Block(models.Model):
    timestamp = models.DateTimeField(default=datetime.utcnow)
    data = models.TextField()
    previous_hash = models.CharField(max_length=64)
    hash = models.CharField(max_length=64)
    nonce = models.IntegerField(default=0)
    objects = None


    def save(self, *args, **kwargs):

        if block := Block.objects.last():
            self.previous_hash= block.hash
        else:
            self.previous_hash="0"
        self.hash= self.compute_hash

        super().save(*args, **kwargs)


    def __str__(self):
        return f'Block {self.id} : {self.data}'


    @property
    def compute_hash(self):
        block_data = json.dumps({
            "id": self.id,
            "timestamp": str(self.timestamp),
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_data).hexdigest()


    @staticmethod
    def get_latest_block():
        return Block.objects.order_by('-id').first()

class CreateMine(models.Model):
    block = models.OneToOneField (Block, on_delete= models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    previous_hash = models.CharField(max_length=64, blank=True, null=True)
    data = models.TextField()
    hash = models.CharField(max_length=64, unique=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = self.calculate_hash()
        super().save(*args, **kwargs)

    def calculate_hash(self):
        block_string = f"{self.timestamp}{self.previous_hash}{self.data}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def __str__(self):
        return f"Block {self.id} - Hash: {self.hash[:10]}..."


class BlockchainEntry(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField(default='default@example.com')
    customer_address = models.CharField(max_length=255, null=True)
    order_date = models.DateTimeField(default=now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, default='cash')
    timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer_name}"

def default_profile_pic():
    return "blockchain/profile_pics/default.png"

class Profile(models.Model):
    objects = None
    user = models.OneToOneField(
        User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(
        upload_to='blockchain/profile_pics/',
        default='blockchain/profile_pics/default.png',
        null=True,
        blank=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return f"{self.user.username} {_('profile')}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_pic.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)
