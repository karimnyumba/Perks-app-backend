from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .Serializers import UserSerializer, ChangePasswordSerializer
from django.contrib.auth import authenticate, login, update_session_auth_hash
from .tokens import get_user_token
from .models import User
from rest_framework.generics import UpdateAPIView


class RegisterUser(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        data = request.data
        print(request.data)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            email = data['email']
            user = User.objects.filter(email=email)
            if user:
                message = {'status': False, 'message': 'Username already exists'}
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.save()

            message = {'save': True}
            return Response(message)

        message = {'save': False, 'errors': serializer.errors}
        return Response(message)
# {
# "fname":"Hassan",
# "lname":"Hassan",
# "email":"hassan@gm++++++++++++++.com",
# "password":"ha+++++++++++++++++++++3",
# "username":"hassaan",
# "phone_number":"078676726",
# "role":1,
# "gender":"L"
# }


class LoginView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        print('Data: ', phone_number, password)
        user = authenticate(phone_number=phone_number, password=password)
        if user is not None:
            login(request, user)
            user_id = User.objects.get(phone_number=phone_number)
            user_info = UserSerializer(instance=user_id, many=False).data
            response = {
                'token': get_user_token(user_id),
                'user': user_info
            }

            return Response(response)
        else:
            response = {
                'msg': 'Invalid username or password',
            }

            return Response(response)
#
# {
#     "phone_number":"255712177151",
#     "password":"2+++++++++++++++++++++++++++++++5"
# }


class UserInformation(APIView):

    @staticmethod
    def get(request, query_type):
        if query_type == 'single':
            try:
                user_id = request.GET.get('user_id')
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'message': 'User Does Not Exist'})
            return Response(UserSerializer(instance=user, many=False).data)

        elif query_type == 'all':
            queryset = User.objects.all()
            return Response(UserSerializer(instance=queryset, many=True).data)

        else:
            return Response({'message': 'Wrong Request!'})


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        gender = request.data['gender']
        email = request.data['email']
        fname = request.data['fname']
        lname = request.data['lname']
        phone_number = request.data['phone_number']
        if request.user.username == email:
            try:
                query = User.objects.get(email=email)
                query.email = email,
                query.fname = fname
                query.lname = lname
                query.phone_number = phone_number
                query.save()
                return Response({'message': 'success'})
            except User.DoesNotExist:
                return Response({'message': 'You can not change the email'})

        else:

            return Response({'message': 'Not Authorized to Update This User'})


