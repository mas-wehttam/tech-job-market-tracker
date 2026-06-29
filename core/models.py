from django.db import models


class JobPost(models.Model):
    title =  models.CharField(max_length=255)
    link = models.URLField(unique=True)
    scraped_at = models.DateTimeField(auto_now_add=True)  

    raw_salary = models.TextField(null=True, blank=True)
    raw_date_posted = models.TextField(null=True, blank=True)
    required_skills = models.TextField(null=True, blank=True)

    min_salary = models.IntegerField(null=True, blank=True)
    max_salary = models.IntegerField(null=True, blank=True)
    currency = models.CharField(max_length=10, blank=True, null=True)
    salary_period = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title
    






