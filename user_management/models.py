from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# Create your models here.
class User(AbstractUser):
    ADMIN = 1
    CUSTOMER = 2
    VENDOR = 3
    ROLE_CHOICES = (
        (ADMIN, "System admin"),
        (CUSTOMER, "resturant customer"),
        (VENDOR, "vendor admin")
    )
    GENDER = (
        ("M", "MALE"),
        ("F", "FEMALE")
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fname = models.CharField(max_length=100, blank=True)
    lname = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    gender = models.CharField(choices=GENDER, null=True, blank=True, max_length=6)
    profile = models.ImageField(upload_to="uploads/", null=True, blank=True)
    role = models.PositiveIntegerField(choices=ROLE_CHOICES, default=CUSTOMER)
    created_at = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=12, default="255 716 058802")
    total_points_made = models.PositiveIntegerField(default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['fname', 'phone_number', 'lname', 'username']
    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'

