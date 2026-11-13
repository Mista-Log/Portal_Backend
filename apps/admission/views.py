from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Application
from .permissions import REVIEWER_ROLES, ApplicationPermission
from .serializers import (
    ApplicationReviewSerializer,
    ApplicationSerializer,
)


def applications_for(user):
    """
    Officers and the registrar see every application.
    Everyone else only sees their own.
    """
    queryset = (
        Application.objects
        .select_related("owner")
        .prefetch_related("qualifications")
    )

    if user.role in REVIEWER_ROLES:
        return queryset

    return queryset.filter(owner=user)


class ApplicationListCreateView(generics.ListCreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [ApplicationPermission]

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        "application_number",
        "owner__email",
        "owner__first_name",
        "owner__last_name",
    ]
    ordering_fields = ["created_at", "session"]

    def get_queryset(self):
        return applications_for(self.request.user)

    def perform_create(self, serializer):
        # The owner always comes from the logged-in user,
        # never from the request body.
        serializer.save(owner=self.request.user)


class ApplicationDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [ApplicationPermission]
    http_method_names = ["get", "patch", "head", "options"]

    def get_queryset(self):
        return applications_for(self.request.user)

    def get_serializer_class(self):
        if self.request.method == "PATCH":
            return ApplicationReviewSerializer
        return ApplicationSerializer

    def update(self, request, *args, **kwargs):
        application = self.get_object()

        serializer = ApplicationReviewSerializer(
            application,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # Return the full application, not just the two fields.
        return Response(
            ApplicationSerializer(
                application,
                context={"request": request},
            ).data
        )


class MyApplicationView(APIView):
    """
    Return the logged-in user's most recent application.
    """

    permission_classes = [ApplicationPermission]

    @extend_schema(
        tags=["Applications"],
        summary="Get my application",
        description="Returns the logged-in user's most recent application.",
        responses={
            200: ApplicationSerializer,
            404: OpenApiResponse(
                description="You have not submitted an application."
            ),
        },
    )
    def get(self, request):
        application = (
            applications_for(request.user)
            .filter(owner=request.user)
            .first()
        )

        if application is None:
            return Response(
                {"detail": "You have not submitted an application."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            ApplicationSerializer(
                application,
                context={"request": request},
            ).data
        )