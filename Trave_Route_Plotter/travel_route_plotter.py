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

    map_to_draw.drawmapboundary(fill_color='#5D9BFF')
    map_to_draw.fillcontinents(color='white', lake_color='blue')
    map_to_draw.drawcountries(color='#585858', linewidth=1)
    map_to_draw.drawstates(linewidth=0.2)
    map_to_draw.drawcoastlines()

    if __name__ == '__main__':
        plt.show()

    return plt


def create_map_with_points(map_points_list: list):
    plt.figure(figsize=(20, 20))

    m = Basemap(projection='merc', llcrnrlon=-180, llcrnrlat=10, urcrnrlon=-50,
                urcrnrlat=70, lat_ts=0, resolution='l')

    points = {}
    for map_point in map_points_list:
        assert isinstance(map_point, MapPoint)
        points.__setitem__(map_point.Name, (map_point.Latitude, map_point.Longitude))

    lon = [points[key][0] for key in points]
    lat = [points[key][1] for key in points]

    x, y = m(lat, lon)
    m.scatter(x, y, zorder=5, s=200, color="#DE1D1D", marker="^")
    return m, lon, lat


def create_map_with_roads(map_points_list: list):
    m, lon, lat = create_map_with_points(map_points_list)

    for index in range(len(lon) - 1):
        x, y = m.gcpoints(lat[index], lon[index], lat[index + 1], lon[index + 1], 500)
        plt.plot(x, y, color="#E59D59", linewidth=2)

    return m


def main():
    places_list = ["New York", "Washington DC", "Los Angeles", "San Francisco"]
    map_points_list = [MapPoint(name) for name in places_list]
    # map_to_draw = create_map_with_points(places_list)
    map_to_draw = create_map_with_roads(map_points_list)
    draw_map(map_to_draw)


def get_map_with_roads_as_graph(places_list: list):
    map_points_list = [MapPoint(name) for name in places_list]
    map_to_draw = create_map_with_roads(map_points_list)
    plotted_map = draw_map(map_to_draw)

    return plotted_map


if __name__ == '__main__':
    main()
