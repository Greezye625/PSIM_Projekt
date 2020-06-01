from geopy.geocoders import Nominatim
import matplotlib
import matplotlib.pyplot as plt
import json
from mpl_toolkits.basemap import Basemap
import matplotlib.colors as colors
from geopy.distance import geodesic
from Trave_Route_Plotter.tsp_calculation import travellingSalesmanProblem
from collections import OrderedDict


class MapPoint:
    def __init__(self, Name: str):
        self.Name = Name
        self.Latitude, self.Longitude = get_latitude_and_longitude_for_location(self.Name)

    def get_geolocation(self):
        return self.Latitude, self.Longitude


def get_latitude_and_longitude_for_location(location_name: str):
    geolocator = Nominatim(user_agent="PSIM")
    location = geolocator.geocode(location_name)

    return location.latitude, location.longitude




def draw_map(map_to_draw):
    if isinstance(map_to_draw, tuple):
        map_to_draw = map_to_draw[0]

    try:
        map_to_draw.drawmapboundary(fill_color='#a2e8d9')
    except:
        pass
    try:
        map_to_draw.fillcontinents(color='#72c963', lake_color='#00ccff')
    except:
        pass
    try:
        map_to_draw.drawcountries(color='#585858', linewidth=3)
    except:
        pass
    try:
        map_to_draw.drawstates(linewidth=1)
    except:
        pass
    try:
        map_to_draw.drawcoastlines()
    except:
        pass

    if __name__ == '__main__':
        plt.show()

    return plt


def find_border_values_for_map_corners(points_list: list):

    tmp_points_list = sorted(points_list,key=(lambda x: x.Latitude))
    min_lat_point, max_lat_point = tmp_points_list[0], tmp_points_list[-1]

    tmp_points_list.sort(key=(lambda x: x.Longitude))
    min_lon_point, max_lon_point = tmp_points_list[0], tmp_points_list[-1]

    return max_lat_point.Latitude+1, max_lon_point.Longitude+2, min_lat_point.Latitude-1, min_lon_point.Longitude-2


def create_map_with_points(map_points_list: list):
    plt.figure(figsize=(20, 20))

    max_lat, max_lon, min_lat, min_lon = find_border_values_for_map_corners(map_points_list)

    m = Basemap(projection='merc', llcrnrlon=min_lon, llcrnrlat=min_lat, urcrnrlon=max_lon,
                urcrnrlat=max_lat, lat_ts=0, resolution='i')

    points = {}
    for map_point in map_points_list:
        assert isinstance(map_point, MapPoint)
        points.__setitem__(map_point.Name, (map_point.Latitude, map_point.Longitude))

    lon = [points[key][0] for key in points]
    lat = [points[key][1] for key in points]

    x, y = m(lat, lon)
    m.scatter(x, y, zorder=5, s=20, color="#DE1D1D", marker=".")

    for i, point in enumerate(map_points_list):
        try:
            plt.annotate(f"{i+1}. {point.Name}", (x[i], y[i]))
        except:
            pass

    return m, lon, lat


def create_map_with_roads(map_points_list: list):
    m, lon, lat = create_map_with_points(map_points_list)

    for index in range(len(lon) - 1):
        x, y = m.gcpoints(lat[index], lon[index], lat[index + 1], lon[index + 1], 500)
        plt.plot(x, y, color="#E59D59", linewidth=3)

    if len(map_points_list) > len(lon):
        x, y = m.gcpoints(lat[-1], lon[-1], lat[0], lon[0], 500)
        plt.plot(x, y, color="#E59D59", linewidth=3)

    return m



def create_distance_matrix(map_points: list):
    distance_matrix = []

    for start_point in map_points:

        start_distance_list = []

        for end_point in map_points:
            assert isinstance(start_point, MapPoint)
            assert isinstance(end_point, MapPoint)

            if start_point is end_point:
                start_distance_list.append(0)
            else:
                distance = geodesic(start_point.get_geolocation(), end_point.get_geolocation()).kilometers
                start_distance_list.append(distance)

        distance_matrix.append(start_distance_list)


    return distance_matrix


def remove_duplicates(places_list: list):
    # from python3.7 dictionary is guaranteed to maintain insertion order
    return list(dict.fromkeys(places_list))


def get_places_sorted_for_best_route(places_list):

    if places_list[0] == places_list[-1]:
        places_list.pop(-1)
        round_trip = True
    else:
        round_trip = False

    places_list = remove_duplicates(places_list)
    map_points_list = [MapPoint(name) for name in places_list]


    distance_matrix = create_distance_matrix(map_points_list)

    distance, order_of_visiting = travellingSalesmanProblem(matrix=distance_matrix,
                                                            start_point=0,
                                                            round_trip=round_trip)

    ordered_places_list = []

    for i in order_of_visiting:
        ordered_places_list.append(map_points_list[i])


    return ordered_places_list


def get_map_with_roads_as_basemap_graph(places_list: list):
    sorted_map_points_list = get_places_sorted_for_best_route(places_list)


    map_to_draw = create_map_with_roads(sorted_map_points_list)
    plotted_map = draw_map(map_to_draw)

    return plotted_map, [point.Name for point in sorted_map_points_list]



def main():
    # places_list = ["New York", "Washington DC", "Los Angeles", "San Francisco"]
    places_list = ["katowice", "wrocław", "kraków", "warszawa", "wrocław", "opole", "malbork", "katowice"]

    sorted_map_points_list = get_places_sorted_for_best_route(places_list)


    map_to_draw = create_map_with_roads(sorted_map_points_list)
    draw_map(map_to_draw)



if __name__ == '__main__':
    main()
