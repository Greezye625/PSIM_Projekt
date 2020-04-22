from django.shortcuts import render
from Trave_Route_Plotter import travel_route_plotter
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_IMG_DIR = os.path.join(BASE_DIR, 'static', 'images')


# Create your views here.


def home(request):
    return render(request, 'home.html')


def plan_journey(request):
    return render(request, 'travel_planner/plan_journey.html')


def result(request):
    places_list = ["New York", "Washington DC", "Los Angeles", "San Francisco"]
    plotted_map = travel_route_plotter.get_map_with_roads_as_graph(places_list)

    plotted_map.savefig(os.path.join(RESULT_IMG_DIR, "result_map.png"), bbox_inches='tight', pad_inches=0)

    return render(request, 'travel_planner/result.html')
