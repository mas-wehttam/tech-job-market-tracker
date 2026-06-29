import django_filters
from .models import JobPost


class JobPostFilter(django_filters.FilterSet):
    class Meta:
        model = JobPost
        fields = {
            'title': ['icontains'],
            'required_skills': ['icontains'],
            'min_salary': ['gte', 'lte'],
            'max_salary': ['gte', 'lte'],
            'currency': ['exact'],
            'salary_period': ['exact'],
            'id': ['range'],
        }






