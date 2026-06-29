from django.shortcuts import render


def job_dashboard(request):
    return render(request, 'core/dashboard.html')



