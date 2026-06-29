from rest_framework import viewsets
from .models import JobPost
from .serializers import JobPostSerializer
from .paginations import CustomPagination
from .filters import JobPostFilter


class JobPostViewset(viewsets.ReadOnlyModelViewSet):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    pagination_class = CustomPagination
    filterset_class = JobPostFilter

    search_fields = ['title', 'required_skills']
    ordering_fields = ['min_salary', 'max_salary', 'scraped_at']






