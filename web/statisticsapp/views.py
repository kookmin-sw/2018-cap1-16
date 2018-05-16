from django.shortcuts import render

def statistics_view(request):
    return render(request, "statistics.html")
