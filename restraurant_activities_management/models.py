from django.db import models
from user_management.models import User
import uuid


class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    pic = models.ImageField(upload_to="uploads/", null=True, blank=True)
    reg_no = models.CharField(max_length=20, unique=True)
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
    pic = models.ImageField(upload_to="uploads/", null=True, blank=True)
    product = models.CharField(max_length=200)
    points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product}'

    class Meta:
        db_table = "award"


class Transactions(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points_made = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class AwardsCount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    award = models.ForeignKey(Award, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    award_code = models.PositiveIntegerField()
    code_used_state = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  null=True, blank=True, db_column='user_id')

    def __str__(self):
        return f'{self.id}'

    class Meta:
        db_table = "awardcount"


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
    total_lifetime_points = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        db_table = "user_restraurant"
