import random
import smtplib
import tempfile
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from rest_framework.response import Response
from .models import *
from .serializer import *
from rest_framework.views import APIView


class RestaurantView(APIView):

    @staticmethod
    def post(request):
        data = request.data
        serialized = RestraurantPostSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            restaurant_added = Restaurant.objects.get(reg_no=serialized['reg_no'].value)
            all_users = User.objects.all()
            for user in all_users:
                user_rt_serialized = UserRestraurantPostSerializer(data={
                    "user": user.id,
                    "restraurant": restaurant_added.id,
                    "total_points": 0
                })
                if user_rt_serialized.is_valid():
                    user_rt_serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = Restaurant.objects.all()
            serialized = RestraurantGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "single":
            userId = request.GET.get("userId")
            queryset = Restaurant.objects.filter(user=userId)
            serialized = RestraurantGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})

    # {
    #     "name": "Shishi food",
    #     "location":"Dodoma",
    #     "reg_no": "1111111"
    # }


class CouponView(APIView):

    @staticmethod
    def post(request):
        data = request.data
        serialized = CouponPostSerializer(data=data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        if querytype == "all":
            queryset = Coupon.objects.all()
            serialized = CouponGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        if querytype == "single":
            couponId = request.GET.get("coupon")
            queryset = Coupon.objects.get(id=couponId)
            serialized = CouponGetSerializer(instance=queryset)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})

    # {
    #     "restraurant": "00d749d0-e++++++++++++++++++++++++490-784d34a3e0ce",
    #     "start_amount":1000,
    #     "end_amount": 2000,
    #     "coupon_no": "1111111",
    #     "point": 100
    # }


class AwardView(APIView):

    @staticmethod
    def post(request):
        data = request.data
        reward_threshold = int(data.get("threshold"))
        reward_ratio = 0.5
        reward_value = int(data.get("reward_value"))
        numbers_of_points = (reward_threshold * reward_ratio) / reward_value
        award_data = {
            "restraurant": data.get("restraurant"),
            "pic": data.get("pic"),
            "product": data.get("product"),
            "points": int(numbers_of_points)
        }
        serialized = AwardPostSerializer(data=award_data)
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        restraurantId = request.GET.get("restraurantId")
        queryset = Award.objects.filter(restraurant=restraurantId)
        serialized = AwardGetSerializer(instance=queryset, many=True)
        return Response(serialized.data)

    # {
    #     "restraurant": "00d749d0-eb33-40d0-=======demkjks-----------784d34a3e0ce",
    #     "product":"Burger",
    #     "point": 1000
    # }


class GenerateRewards(APIView):

    @staticmethod
    def post(request):
        data = request.data
        awardcount = int(data.get('count'))

        for num in range(0, awardcount):
            award_data = {
                "award": data.get('award'),
                "award_code": random.randint(1001, 9998),
                "code_used_state": False
            }
            serialized = AwardCountPostSerializer(data=award_data)
            if serialized.is_valid():
                serialized.save()
        return Response({"save": True})

    @staticmethod
    def get(request):
        querytype = request.GET.get("querytype")
        award = request.GET.get("award")
        award_id = request.GET.get("id")
        user_id = request.GET.get("user")
        print(award_id)
        if querytype == "award":
            queryset = AwardsCount.objects.filter(award=award)
            serialized = AwardCountGetSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        elif querytype == "use_award":
            try:
                user = User.objects.get(id=user_id)
                award_wanted = AwardsCount.objects.get(id=award_id)
                award_wanted.code_used_state = True
                award_wanted.user = user
                award_wanted.save()
                return Response({"success": True, "award_code": award_wanted.award_code})
            except AwardsCount.DoesNotExist:
                return Response({"success": False, "award_code": "The award is not available or already used"})
        elif querytype == "user_redeemed_rewards":
            queryset = AwardsCount.objects.filter(user=user_id).order_by('-created_at')[:5]
            serialized = AwardCountGetTopSerializer(instance=queryset, many=True)
            return Response(serialized.data)
        else:
            return Response({"message": "Specify the querying type"})


class Recommendations(APIView):
    @staticmethod
    def post(request):
        try:
            data = request.data
            recommendationtext = data.get('recommendationText')
            print(recommendationtext)

            # SMTP configuration
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            smtp_username = "perks255@gmail.com"
            smtp_password = "erdr gaxc agkh qyxg"
            smtp_sender = "perks255@gmail.com"
            smtp_recipient = "perks255@gmail.com"

            # Create a message object
            # message = MIMEMultipart()
            # message['From'] = "perks225@gmail.com"
            # message['To'] = "perks225@gmail.com"
            # message['Subject'] =

            # message.attach(MIMEText(recommendationtext, 'plain'))
            msg = MIMEText(recommendationtext)
            msg['Subject'] = 'RECOMMENDATION EMAIL'
            msg['From'] = smtp_sender
            msg['To'] = ', '.join(smtp_recipient)
            #  msg = MIMEText(body)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
               smtp_server.login(smtp_username, smtp_password)
               smtp_server.sendmail(smtp_username, smtp_recipient, msg.as_string())
            print("Message sent!")

            return Response({'message': "Email sent successfully!"})
        except Exception as e:
            return Response({'message': f"Email sending failed: {str(e)}"})


class CouponTransactionView(APIView):

    @staticmethod
    def post(request):
        data = request.data
        print(data)
        points_used = int(data.get("point_used"))
        trans_data = {
            "user": data.get("user"),
            "award": data.get("award"),
            "point_used": points_used
        }
        print(data.get("restaurant_id"))
        serialized = CouponTransactionPostSerializer(data=trans_data)
        user_restaurant = UserRestraurant.objects.get(user=data.get("user"), restraurant=data.get("restaurant_id"))
        user = User.objects.get(id=data.get("user"))
        user.total_points_made -= points_used
        user_restaurant.total_points -= points_used
        user_restaurant.save()
        user.save()
        if serialized.is_valid():
            serialized.save()
            return Response({"save": True})
        return Response({"save": False, "error": serialized.errors})

    @staticmethod
    def get(request):
        userId = request.GET.get("userId")
        queryset = CouponTransaction.objects.filter(user=userId)
        serialized = CouponTransactionGetSerializer(instance=queryset, many=True)
        return Response(serialized.data)

    # {
    #     "user": "00d749d0-+++DEMO+++-0-784d34a3e0ce",
    #     "award": "00d749d0-+++DEMO+++-0-784d34a3e0ce",
    #     "point_used": 1000
    # }


class UserRestraurantView(APIView):

    @staticmethod
    def post(request):
        data = request.data
        user_id = data.get('user')
        restaurant_id = data.get('restraurant')
        total_points = data.get('total_points')
        try:
            user_restaurant = UserRestraurant.objects.get(user=user_id, restraurant=restaurant_id)
            transactioned = TransactionPostSerializer(data={
                "user": user_id,
                "coupon": data.get('coupon'),
                "points_made": total_points
            })
            if transactioned.is_valid():
                transactioned.save()
            print(user_restaurant)
            user_restaurant.total_points += total_points
            user_restaurant.total_lifetime_points += total_points
            user = User.objects.get(id=user_id)
            user.total_points_made += total_points
            user.total_lifetime_points += total_points
            user.save()
            user_restaurant.save()
        except UserRestraurant.DoesNotExist:
            serialized = UserRestraurantPostSerializer(data=data)
            if serialized.is_valid():
                serialized.save()
                return Response({"save": True})

        return Response({"save": True, "msg": "The Points added to the user"})

    @staticmethod
    def get(request):
        userId = request.GET.get("userId")
        queryset = UserRestraurant.objects.filter(user=userId)
        serialized = UserRestraurantGetSerializer(instance=queryset, many=True)
        return Response(serialized.data)

    # {
    #     "user": "00d749d0-+++DEMO+++-0-784d34a3e0ce",
    #     "restraurant": "00d749d0-+++DEMO+++-0-784d34a3e0ce",
    #     "total_points": 1000
    # }


class DashboardData(APIView):
    @staticmethod
    def get(request, userId):
        userRestraurants = UserRestraurant.objects.filter(user=userId)
        total_ponts = 0
        for data in userRestraurants:
            total_ponts = total_ponts + data.total_points
        response = {"total_points": total_ponts}
        return Response(response)
