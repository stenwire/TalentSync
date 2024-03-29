from rest_framework import status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, RegisterSerializer, TokenSerializer


class RegisterView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        data = request.data
        content_type = request.content_type

        if content_type == "application/x-www-form-urlencoded":
            data = dict(request.data)

        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        # serializer.save()
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        token_serializer = TokenSerializer(
            {"refresh": str(refresh), "access": str(refresh.access_token)}
        )

        return Response(token_serializer.data)


class TokenRefreshView(views.APIView):
    def post(self, request, format=None):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = RefreshToken(serializer.validated_data["refresh"])
        token_serializer = TokenSerializer(
            {"refresh": str(refresh), "access": str(refresh.access_token)}
        )
        return Response(token_serializer.data)
