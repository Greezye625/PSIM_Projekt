from django.db import models
from django.contrib.auth.models import User


# Create your models here.


# class UserProfile(models.Model):
#
#     user = models.OneToOneField(User, models.CASCADE)
#
#     dummyfield = models.CharField(max_length=264)
#
#
#     def __str__(self):
#         return self.user.username


class TravelRoute(models.Model):
    User = models.ForeignKey(User, models.CASCADE, null=True)
    Start_point = models.CharField(max_length=264)
    Mid_points = models.TextField(max_length=1024, null=True, blank=True)
    End_point = models.CharField(max_length=264)
    Route = models.CharField(max_length=1536)
    Public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.Start_point} - {self.Mid_points} - {self.End_point}"

    def to_dict(self):
        return {'User': self.User.username,
                "Start_point": self.Start_point,
                "Mid_points": self.Mid_points,
                "End_point": self.End_point,
                "Route": self.Route,
                "Public": self.Public,
                }



class PointOfInterest(models.Model):
    poi_name = models.CharField(max_length=256)
    latitude = models.FloatField()
    longitude = models.FloatField()
    num_links = models.IntegerField()
    links = models.CharField(max_length=1024)
    num_categories = models.IntegerField()
    categories = models.CharField(max_length=512)

    def __str__(self):
        return f'{self.poi_name} ({self.latitude}    {self.longitude})'


    def to_dict(self):
        return {'poi_name': self.poi_name,
                'latitude': self.latitude,
                'longitude': self.longitude,
                'num_links': self.num_links,
                'links': self.links,
                'num_categories': self.num_categories,
                'categories': self.categories,
                }

