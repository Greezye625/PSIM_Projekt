import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from Trave_Route_Plotter import travel_route_plotter
import os
from travel_planner.forms import NewTravelRouteForm, UserForm
import re
from travel_planner.models import TravelRoute, User, PointOfInterest
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_IMG_DIR = os.path.join(BASE_DIR, 'static', 'images')


# Create your views here.

def home(request):
    return render(request, 'home.html')


# @login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@csrf_exempt
def change_public_state(request):
    if request.method == "POST":
        route = TravelRoute.objects.get(pk=int(request.GET['id']))

        if route.Public:
            route.Public = False
        else:
            route.Public = True

        route.save()

    request.method = 'GET'
    return result(request)


@csrf_exempt
def registration(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(request.POST)

        mobile = request.POST.get('mobile')

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True

            if mobile:
                return HttpResponse(f"Registered,{user.username}")

        else:
            print(user_form.errors)

    else:
        user_form = UserForm()

    return render(request, 'travel_planner/registration.html', context={'user_form': user_form,
                                                                        'registered': registered})


# @login_required
@csrf_exempt
def plan_journey(request):
    form = NewTravelRouteForm()

    if request.method == "POST":
        mobile = request.POST.get('mobile')

        form = NewTravelRouteForm(request.POST)

        if form.is_valid():
            if mobile:
                user = User.objects.get(username=request.POST.get('user'))
            else:
                user = request.user

            form.instance.User = user
            form.save(commit=True)

            return result(request)
        else:
            print("Error")

    return render(request, 'travel_planner/plan_journey.html', context={'form': form})


# @login_required
@csrf_exempt
def result(request):
    if request.method == "POST":
        startpoint = request.POST['Start_point']
        places_list = [startpoint]

        if request.POST['Mid_points']:
            midpoints = re.split(r"[,.\-_] *", request.POST['Mid_points'])
            places_list += midpoints

        endpoint = request.POST['End_point']
        places_list.append(endpoint)

        places_list = [item.capitalize() for item in places_list]

        places_list = travel_route_plotter.get_best_road(places_list)

        route_obj = TravelRoute.objects.last()
        route_obj.Route = places_list
        route_obj.save()

        if request.POST.get('mobile'):
            sorted_route_msg = ''
            for point in places_list:
                sorted_route_msg += f'{point},'
            sorted_route_msg = sorted_route_msg[:-1]

            return HttpResponse(sorted_route_msg)

        # plotted_map, places_list = travel_route_plotter.get_map_with_roads_as_basemap_graph(places_list)


    elif request.method == "GET":
        route_obj = TravelRoute.objects.get(pk=request.GET['id'])
        places_list_str = route_obj.Route
        re_list = re.findall(r'[a-ząćęłńóśżźA-ZĄĆĘŁŃÓŚŻŹ\s-]*', places_list_str)
        places_list = list(filter(lambda x: x not in [' ', ''], re_list))

    plotted_map = travel_route_plotter.get_map_with_roads_as_basemap_graph(places_list)

    plotted_map.savefig(os.path.join(RESULT_IMG_DIR, "result_map.png"), bbox_inches='tight', pad_inches=0)
    context_dict = {'places_list': places_list, 'route_obj': route_obj}

    return render(request, 'travel_planner/result.html', context=context_dict)


@csrf_exempt
def user_profile_page(request):
    if request.GET.get('mobile'):
        user = User.objects.get(username=request.GET['username'])
    else:
        user = request.user
    routes = TravelRoute.objects.filter(User=user)

    if request.GET.get('mobile'):
        routes_dict = {obj.id: obj.to_dict() for obj in routes}
        return JsonResponse(routes_dict)
    else:
        return render(request, 'travel_planner/user_profile_page.html', context={'routes': routes})

@csrf_exempt
def public_routes(request):
    routes = TravelRoute.objects.filter(Public=True)
    if request.GET.get('mobile'):
        routes_dict = {obj.id: obj.to_dict() for obj in routes}
        return JsonResponse(routes_dict)
    else:
        return render(request, 'travel_planner/public_routes.html', context={'routes': routes})


@csrf_exempt
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                mobile = request.POST.get('mobile')
                if mobile:
                    return HttpResponse(f"Logged In,{user}")
                else:
                    return HttpResponseRedirect(reverse('travel_planner:plan_journey'))

            else:
                return HttpResponse("Account not active")

        else:
            print("Someone tried to login and failed")
            print(f"Username: {username}\npassword {password}")
            return HttpResponse("Invalid login info")

    else:
        return render(request, 'travel_planner/login.html', context={})


@csrf_exempt
def poi(request):
    if request.method == "GET":
        min_lat = request.GET['min_lat']
        min_lon = request.GET['min_lon']
        max_lat = request.GET['max_lat']
        max_lon = request.GET['max_lon']

        points_of_interest = PointOfInterest.objects.filter(latitude__gt=min_lat, latitude__lt=max_lat, longitude__gt=min_lon, longitude__lt=max_lon)
        poi_dict = {obj.id: obj.to_dict() for obj in points_of_interest}

        return JsonResponse(poi_dict)
