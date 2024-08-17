from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from users.serializers import UserSerializer, LoginSerializer


@api_view(["POST"])
def login(request):
    login_serializer = LoginSerializer(data=request.data)
    login_serializer.is_valid(raise_exception=True)

    user = authenticate(
        request,
        username=login_serializer.validated_data["username"],
        password=login_serializer.validated_data["password"],
    )
    if user is None:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    token = RefreshToken.for_user(user)
    return Response(
        {
            "refresh": str(token),
            "access": str(token.access_token),
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def logout(request):
    try:
        token = RefreshToken(request.data.get("refresh", ""))
        token.blacklist()
    except TokenError:
        return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def refresh(request):
    try:
        token = RefreshToken(request.data.get("refresh", ""))
        access_token = str(token.access_token)
    except TokenError:
        return Response({"message": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
    return Response(
        {
            "access": access_token,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
