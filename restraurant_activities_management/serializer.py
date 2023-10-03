from rest_framework import serializers
from .models import *

class RestraurantGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"
        depth = 2


class RestraurantPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            "name",
            "location",
            "reg_no",
        ]
        

class CouponGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"
        depth = 2


class CouponPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = [
            "restraurant",
            "start_amount",
            "end_amount",
            "coupon_no",
            "point",
        ]


class AwardGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = "__all__"
        depth = 2


class AwardPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = [
            "restraurant",
            "product",
            "points",
            "pic"
        ]


class AwardCountGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwardsCount
        fields = "__all__"


class AwardCountPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwardsCount
        fields = [
            "award",
            "award_code",
            "code_used_state"
        ]

        
class CouponTransactionGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponTransaction
        fields = "__all__"
        depth = 2


class CouponTransactionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponTransaction
        fields = [
            "user",
            "award",
            "point_used",
        ]
        

class UserRestraurantGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRestraurant
        fields = "__all__"
        depth = 2


class UserRestraurantPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRestraurant
        fields = [
            "user",
            "restraurant",
            "total_points",
        ]