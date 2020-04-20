from django.shortcuts import render


# Create your views here.


def home(request):
    return render(request, 'home.html')


def plan_journey(request):
    return render(request, 'travel_planner/plan_journey.html')


def result(request):
    return render(request, 'travel_planner/result.html')
