from django.shortcuts import render # pyright: ignore[reportMissingModuleSource]
from django.shortcuts import get_object_or_404
from .models import User, UserRole
from .serializers import StudentSerializer
# Create your views here.
from rest_framework.views import APIView # pyright: ignore[reportMissingImports]
from rest_framework.response import Response # type: ignore
from rest_framework import status # pyright: ignore[reportMissingImports]
from rest_framework.permissions import AllowAny, IsAuthenticated # pyright: ignore[reportMissingImports]

from rest_framework_simplejwt.tokens import RefreshToken # pyright: ignore[reportMissingImports]
from rest_framework_simplejwt.exceptions import TokenError # pyright: ignore[reportMissingImports]

from drf_spectacular.utils import ( # pyright: ignore[reportMissingImports]
    extend_schema,
    OpenApiResponse,
)

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    LogoutSerializer,
    TokenResponseSerializer,
    StudentSerializer,
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


class StudentListView(APIView):
    """
    Retrieve all student records.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Students"],
        summary="Retrieve all students",
        description="Returns all users whose role is STUDENT.",
        responses={200: StudentSerializer(many=True)},
    )
    def get(self, request):
        students = User.objects.filter(
            role=UserRole.STUDENT
        ).order_by("last_name", "first_name")

        serializer = StudentSerializer(
            students,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class StudentDetailView(APIView):
    """
    Retrieve a single student by ID.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Students"],
        summary="Retrieve student details",
        description="Returns a student using their ID.",
        responses={
            200: StudentSerializer,
            404: OpenApiResponse(
                description="Student not found."
            ),
        },
    )
    def get(self, request, pk):
        student = get_object_or_404(
            User,
            pk=pk,
            role=UserRole.STUDENT
        )

        serializer = StudentSerializer(student)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
