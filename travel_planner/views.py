from django.shortcuts import render
from Trave_Route_Plotter import travel_route_plotter
import os
from travel_planner.forms import NewTravelRouteForm, UserForm
import re
from travel_planner.models import TravelRoute
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_IMG_DIR = os.path.join(BASE_DIR, 'static', 'images')


# Create your views here.

def home(request):
    return render(request, 'home.html')



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def registration(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(request.POST)

        if user_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True

        else:
            print(user_form.errors)

    else:
        user_form = UserForm()


    return render(request, 'travel_planner/registration.html', context={'user_form': user_form,
                                                                        'registered': registered})



@login_required
def plan_journey(request):
    form = NewTravelRouteForm()

    if request.method == "POST":
        form = NewTravelRouteForm(request.POST)

        if form.is_valid():
            form.instance.User = request.user
            form.save(commit=True)
            return result(request)
        else:
            print("Error")

    return render(request, 'travel_planner/plan_journey.html', context={'form': form})



@login_required
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

    last = TravelRoute.objects.last()
    last.Route = places_list
    last.save()

    plotted_map.savefig(os.path.join(RESULT_IMG_DIR, "result_map.png"), bbox_inches='tight', pad_inches=0)

    places_dict = {'places_list': places_list}
    return render(request, 'travel_planner/result.html', context=places_dict)



def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('travel_planner:plan_journey'))

            else:
                return HttpResponse("Account not active")

        else:
            print("Someone tried to login and failed")
            print(f"Username: {username}\npassword {password}")
            return HttpResponse("Invalid login info")

    else:
        return render(request, 'travel_planner/login.html', context={})

