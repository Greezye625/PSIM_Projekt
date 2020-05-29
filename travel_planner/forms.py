from django import forms
from travel_planner.models import TravelRoute
from django.contrib.auth.models import User


class NewTravelRouteForm(forms.ModelForm):
    class Meta:
        model = TravelRoute
        fields = ['Start_point', 'Mid_points', 'End_point']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']


# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['dummyfield']