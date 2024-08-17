import uuid

from django.db import models

from users.models import User, Employer


def get_resume_upload_path(_, filename):
    return f"resumes/{uuid.uuid4()}.{filename.split('.')[-1]}"


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Job(models.Model):
    class TimeType(models.TextChoices):
        FULL_TIME = "FT", "Full time"
        PART_TIME = "PT", "Part time"
        HOURLY = "HR", "Hourly"

    class Location(models.TextChoices):
        ON_SITE = "OS", "On site"
        REMOTE = "RM", "Remote"
        HYBRID = "HY", "Hybrid"

    class ContractType(models.TextChoices):
        EMPLOYMENT = "EM", "Employment"
        PROJECT = "PJ", "Project"
        INTERNSHIP = "IN", "Internship"
        SCHOLARSHIP = "SC", "Scholarship"

    class Seniority(models.TextChoices):
        Intern = "IN", "Intern"
        JUNIOR = "JR", "Junior"
        MID = "MD", "Mid"
        SENIOR = "SR", "Senior"
        LEAD = "LD"

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    salary = models.PositiveIntegerField()
    time_type = models.CharField(max_length=2, choices=TimeType.choices)
    seniority = models.CharField(max_length=2, choices=Seniority.choices)
    contract_type = models.CharField(max_length=2, choices=ContractType.choices)
    location = models.CharField(max_length=2, choices=Location.choices)
    expire_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = "PD", "Pending"
        ACCEPTED = "AC", "Accepted"
        REJECTED = "RJ", "Rejected"

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PENDING)
    description = models.TextField()
    resume = models.FileField(upload_to=get_resume_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["job", "applicant"]
