from rest_framework import serializers
from .models import JobPost

class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = [
            'id', 'title', 'link', 'scraped_at', 
            'min_salary', 'max_salary', 'currency', 'salary_period', 
            'required_skills'
        ]







