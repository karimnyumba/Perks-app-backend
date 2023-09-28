from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Coupon)
admin.site.register(Award)
admin.site.register(CouponTransaction)
admin.site.register(UserRestraurant)
