from django.urls import path

from jobs.views import JobView, ApplicationView

app_name = "jobs"

urlpatterns = [
    path("", JobView.as_view(), name="jobs"),
    path("<int:pk>/", JobView.as_view(), name="job"),
    path("applications/", ApplicationView.as_view(), name="applications"),
    path("applications/<int:pk>/", ApplicationView.as_view(), name="application"),
]
