from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User
from . import serializers


class UserInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 회원 정보 수정(비밀번호, 키, 몸무게, 활동량)
    def put(self, request):
        user = request.user
        serializer = serializers.UserPutSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = User.objects.create_user(
                username=request.data["username"],
                password=request.data["password"],
                height=request.data["height"],
                weight=request.data["weight"],
                activity=request.data["activity"],
            )
            updated_serializer = serializers.UserPutSerializer(user)
            return Response(updated_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Signup(APIView):
    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)

        # 회원가입
        if serializer.is_valid():
            user = User.objects.create_user(
                username=request.data["username"],
                password=request.data["password"],
                email=request.data["email"],
                age=request.data["age"],
                gender=request.data["gender"],
                height=request.data["height"],
                weight=request.data["weight"],
                activity=request.data["activity"],
            )
            # recommended_calorie = serializer.get_recommended_calorie(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            return Response(
                {
                    "user": serializers.UserSerializer(user).data,
                    "access": access_token,
                    "refresh": refresh_token,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsernameDuplicate(APIView):
    def post(self, request):
        if User.objects.filter(username=request.data["username"]).exists():
            return Response(
                {"error": "이미 사용중인 닉네임입니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            Response(status=status.HTTP_200_OK)


class EmailDuplicate(APIView):
    def post(self, request):
        if User.objects.filter(email=request.data["email"]).exists():
            return Response(
                {"error": "이미 존재하는 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            Response(status=status.HTTP_200_OK)


# 로그인
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


# 로그아웃
class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# 회원 탈퇴
class Withdrawal(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            user.is_active = False
            user.save()
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
