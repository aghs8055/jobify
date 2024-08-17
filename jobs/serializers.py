from rest_framework import serializers

from jobs.models import Job, Application


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="employer.company_name", read_only=True)
    website = serializers.URLField(source="employer.website", read_only=True)
    address = serializers.CharField(source="employer.address", read_only=True)
    logo = serializers.ImageField(source="employer.logo", read_only=True)
    description = serializers.CharField(source="employer.description", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    time_type_display = serializers.CharField(source="get_time_type_display", read_only=True)
    seniority_display = serializers.CharField(source="get_seniority_display", read_only=True)
    contract_type_display = serializers.CharField(source="get_contract_type_display", read_only=True)
    location_display = serializers.CharField(source="get_location_display", read_only=True)

    class Meta:
        model = Job
        fields = (
            "id",
            "company_name",
            "website",
            "address",
            "logo",
            "description",
            "category_name",
            "time_type_display",
            "seniority_display",
            "contract_type_display",
            "location_display",
            "title",
            "description",
            "salary",
            "expire_at",
            "is_active",
        )


class ApplicationSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Application
        fields = ("id", "job", "status", "description", "resume")
        extra_kwargs = {
            "id": {"read_only": True},
            "status_display": {"read_only": True},
            "description": {"read_only": True},
        }
