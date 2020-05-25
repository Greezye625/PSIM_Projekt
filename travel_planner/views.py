from django.shortcuts import render
from Trave_Route_Plotter import travel_route_plotter
import os
from travel_planner.forms import NewTravelRouteForm
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_IMG_DIR = os.path.join(BASE_DIR, 'static', 'images')


# Create your views here.
# CURRENT_USER =

def home(request):
    return render(request, 'home.html')


def plan_journey(request):
    form = NewTravelRouteForm()

    if request.method == "POST":
        form = NewTravelRouteForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return result(request)
        else:
            print("Error")

    return render(request, 'travel_planner/plan_journey.html', context={'form': form})


def result(request):
    startpoint = request.POST['Start_point']
    places_list = [startpoint]

    if request.POST['Mid_points']:
        midpoints = re.split(r"[,.\-_] *", request.POST['Mid_points'])
        places_list += midpoints

    endpoint = request.POST['End_point']
    places_list.append(endpoint)

    #
    plotted_map, places_list = travel_route_plotter.get_map_with_roads_as_basemap_graph(places_list)

    plotted_map.savefig(os.path.join(RESULT_IMG_DIR, "result_map.png"), bbox_inches='tight', pad_inches=0)

    places_dict = {'places_list': places_list}
    return render(request, 'travel_planner/result.html', context=places_dict)
