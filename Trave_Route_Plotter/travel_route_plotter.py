from geopy.geocoders import Nominatim
import matplotlib
import matplotlib.pyplot as plt
import json
from mpl_toolkits.basemap import Basemap
import matplotlib.colors as colors
import io


class MapPoint:
    def __init__(self, Name: str):
        self.Name = Name
        self.Latitude, self.Longitude = get_latitude_and_longitude_for_location(self.Name)


def get_latitude_and_longitude_for_location(location_name: str):
    geolocator = Nominatim(user_agent="PSIM")
    location = geolocator.geocode(location_name)

    return location.latitude, location.longitude


def draw_map(map_to_draw):
    if isinstance(map_to_draw, tuple):
        map_to_draw = map_to_draw[0]

    map_to_draw.drawmapboundary(fill_color='#a2e8d9')
    map_to_draw.fillcontinents(color='#72c963', lake_color='#00ccff')
    map_to_draw.drawcountries(color='#585858', linewidth=3)
    map_to_draw.drawstates(linewidth=1)
    map_to_draw.drawcoastlines()

    if __name__ == '__main__':
        plt.show()

    return plt


def find_border_values_for_map_corners(points_list: list):
    points_list.sort(key=(lambda x: x.Latitude))
    min_lat_point, max_lat_point = points_list[0], points_list[-1]

    points_list.sort(key=(lambda x: x.Longitude))
    min_lon_point, max_lon_point = points_list[0], points_list[-1]

    return max_lat_point.Latitude+2, max_lon_point.Longitude+2, min_lat_point.Latitude-2, min_lon_point.Longitude-2


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
        plt.annotate(f"{i+1}. {point.Name}", (x[i], y[i]))

    return m, lon, lat


def create_map_with_roads(map_points_list: list):
    m, lon, lat = create_map_with_points(map_points_list)

    for index in range(len(lon) - 1):
        x, y = m.gcpoints(lat[index], lon[index], lat[index + 1], lon[index + 1], 500)
        plt.plot(x, y, color="#E59D59", linewidth=3)

    return m


def main():
    # places_list = ["New York", "Washington DC", "Los Angeles", "San Francisco"]
    places_list = ["Wrocław", "Gdańsk", "Łódź", "Poznań", "Warszawa", "Opole"]
    map_points_list = [MapPoint(name) for name in places_list]
    # map_to_draw = create_map_with_points(places_list)
    map_to_draw = create_map_with_roads(map_points_list)
    draw_map(map_to_draw)


def get_places_sorted_for_best_route(places_list):
    map_points_list = [MapPoint(name) for name in places_list]



    return map_points_list


def get_map_with_roads_as_basemap_graph(places_list: list):
    sorted_map_points_list = get_places_sorted_for_best_route(places_list)
    map_to_draw = create_map_with_roads(sorted_map_points_list)
    plotted_map = draw_map(map_to_draw)

    return plotted_map


if __name__ == '__main__':
    main()
