from django.db import models


# Create your models here.


class User(models.Model):
    Login = models.CharField(max_length=264)
    Password = models.CharField(max_length=264)

    def __str__(self):
        return f'{self.Login}'


class TravelRoute(models.Model):
    User = models.ForeignKey(User, models.CASCADE, null=True)
    Start_point = models.CharField(max_length=264)
    Mid_points = models.TextField(max_length=1024, null=True, blank=True)
    End_point = models.CharField(max_length=264)
    Route = models.CharField(max_length=1536)

    def __str__(self):
        return f"{self.User.Login}: {self.Start_point} - ... - {self.End_point}"
