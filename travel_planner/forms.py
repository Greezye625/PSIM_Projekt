from django import forms
from travel_planner.models import User, TravelRoute


class NewTravelRouteForm(forms.ModelForm):
    class Meta:
        model = TravelRoute
        fields = ['Start_point', 'Mid_points', 'End_point']
