from django.urls import path

from .views import (
    ApplicationListCreateView,
    ApplicationDetailView,
    MyApplicationView,
)


app_name = "admission"

urlpatterns = [
    path(
        "",
        ApplicationListCreateView.as_view(),
        name="application-list",
    ),

    path(
        "me/",
        MyApplicationView.as_view(),
        name="application-me",
    ),

    path(
        "<int:pk>/",
        ApplicationDetailView.as_view(),
        name="application-detail",
    ),
]