from django.db import models
from user_management.models import User
import uuid


class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    reg_no = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        db_table = "Restaurant"


class Coupon(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restraurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    start_amount = models.DecimalField(max_digits=10, decimal_places=2)
    end_amount = models.DecimalField(max_digits=10, decimal_places=2)
    coupon_no = models.CharField(max_length=20)
    points = models.IntegerField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'
    
    class Meta:
        db_table = "coupon"


class Award(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    restraurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'
    
    class Meta:
        db_table = "award"


class CouponTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    award = models.ForeignKey(Award, on_delete=models.CASCADE)
    point_used = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'
    
    class Meta:
        db_table = "coupon_transaction"


class UserRestraurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restraurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    total_points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'
    
    class Meta:
        db_table = "user_restraurant"

    
