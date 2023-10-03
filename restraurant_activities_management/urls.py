from django.urls import path
from .views import *

app_name = 'restraurant_activities_management'

urlpatterns = [
    path('restraurant', RestaurantView.as_view()),
    path('coupon', CouponView.as_view()),
    path('award', AwardView.as_view()),
    path('user-restraurant', UserRestraurantView.as_view()),
    path('user-dashboard/<slug:userId>', DashboardData.as_view()),
    path('generate_rewards', DashboardData.as_view()),
]