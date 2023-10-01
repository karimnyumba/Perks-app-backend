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
    #     "restraurant": "00d749d0-eb33-40d0-a490-784d34a3e0ce",
    #     "start_amount":1000,
    #     "end_amount": 2000,
    #     "coupon_no": "1111111",
    #     "point": 100
    # }



class AwardView(APIView):

    @staticmethod
    def post(request):
        data = request.data
        serialized = AwardPostSerializer(data=data)
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
    #     "restraurant": "00d749d0-eb33-40d0-a490-784d34a3e0ce",
    #     "product":"Burger",
    #     "point": 1000
    # }


class CouponTransactionView(APIView):

    @staticmethod
    def post(request):
        data = request.data
        serialized = CouponTransactionPostSerializer(data=data)
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
            print(user_restaurant)
            user_restaurant.total_points += total_points
            user_restaurant.save()
        except UserRestraurant.DoesNotExist:
            serialized = UserRestraurantPostSerializer(data=data)
            if serialized.is_valid():
                serialized.save()
                return Response({"save": True})

        try:
            user = User.objects.get(id=user_id)
            user.total_points_made += total_points
            user.save()
        except User.DoesNotExist:
            return Response({"save": False, "error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

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
    
    

