from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from jobs.models import Job, Application
from jobs.serializers import JobSerializer, ApplicationSerializer


class JobView(GenericAPIView, ListModelMixin, RetrieveModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Job.objects.filter(expire_at__gte=timezone.now(), is_active=True)

    def get(self, request, pk=None):
        if pk is None:
            return self.list(request)

        return self.retrieve(request)


class ApplicationView(GenericAPIView, ListModelMixin, RetrieveModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = ApplicationSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user)

    def post(self, request):
        serializer = ApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if Application.objects.filter(job=serializer.validated_data["job"], applicant=request.user).exists():
            return Response({"detail": "You have already applied to this job."}, status=400)

        if (
            not serializer.validated_data["job"].is_active
            or serializer.validated_data["job"].expire_at < timezone.now()
        ):
            return Response({"detail": "This job is not active."}, status=400)

        serializer.save(applicant=request.user)
        return Response(serializer.data)

    def get(self, request, pk=None):
        if pk is None:
            return self.list(request)

        return self.retrieve(request)
