from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    LogoutSerializer,
    TokenResponseSerializer,
)


class RegisterView(APIView):
    """
    Register a new student account.
    """

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Authentication"],
        summary="Register a new student",
        description=(
            "Creates a new student account using the supplied "
            "email, first name, last name, and password. "
            "The student role is assigned automatically."
        ),
        request=RegisterSerializer,
        responses={
            201: UserSerializer,
            400: OpenApiResponse(
                description="Validation error."
            ),
        },
    )
    def post(self, request):
        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        response_serializer = UserSerializer(user)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    Authenticate a user and generate JWT tokens.
    """

    permission_classes = [AllowAny]

    @extend_schema(
        tags=["Authentication"],
        summary="Login user",
        description=(
            "Authenticates a user using email and password. "
            "Returns access and refresh JWT tokens."
        ),
        request=LoginSerializer,
        responses={
            200: TokenResponseSerializer,
            400: OpenApiResponse(
                description="Invalid credentials."
            ),
        },
    )
    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={"request": request},
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        response_data = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": UserSerializer(user).data,
        }

        return Response(
            response_data,
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """
    Logout a user by blacklisting their refresh token.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Authentication"],
        summary="Logout user",
        description=(
            "Blacklists the provided refresh token "
            "to prevent it from being used again."
        ),
        request=LogoutSerializer,
        responses={
            205: OpenApiResponse(
                description="Successfully logged out."
            ),
            400: OpenApiResponse(
                description="Invalid or expired refresh token."
            ),
        },
    )
    def post(self, request):
        serializer = LogoutSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        try:
            token = RefreshToken(
                serializer.validated_data["refresh"]
            )

            token.blacklist()

        except TokenError:
            return Response(
                {"detail": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_205_RESET_CONTENT,
        )


class CurrentUserView(APIView):
    """
    Retrieve the authenticated user's information.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Authentication"],
        summary="Get current user",
        description=(
            "Returns the profile information of "
            "the currently authenticated user."
        ),
        responses={
            200: UserSerializer,
            401: OpenApiResponse(
                description="Authentication credentials were not provided."
            ),
        },
    )
    def get(self, request):
        serializer = UserSerializer(request.user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )