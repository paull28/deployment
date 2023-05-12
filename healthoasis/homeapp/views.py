from django.shortcuts import render, redirect

from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from .models import User, Exercise, UserWorkouts

from django.shortcuts import get_object_or_404, redirect, render



from .models import *
from .forms import *

import requests

#WeatherAPI direction dictionary
dir = {
    'NW':'North-West',
    'N':'North',
    'NE':'North-East',
    'E':'East',
    'SE':'South-East',
    'S':'South',
    'SW':'South-West',
    'W':'West'
}

#Nutrition API variables
nutritionAppID = '3cb0640e'
nutritionKey = 'c3fb87d22654be6672e1b78518bd7028'
headers = {'x-app-id':nutritionAppID,
           'x-app-key':nutritionKey,
           'content-type':'application/json'}
nutritionEndPt = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
exerciseEndPt = 'https://trackapi.nutritionix.com/v2/natural/exercise'

#View for homepage
def home(request):
    #WeatherAPI data getter
    weatherResponse = requests.get('http://api.weatherapi.com/v1/current.json?key=59208b37dbca49ae860121639231003&q=Guildford&aqi=no')
    weather = weatherResponse.json()

    try:    #Try to format wind direction nicely
        windDir = dir[weather['current']['wind_dir']]
    except: #Not in pre-def dictionary? Keep as-is
        windDir = weather['current']['wind_dir']

    #NutritionAPI data getter
    nQuery = {
        "query":"big mac"
    }
    nutritionResponse = requests.post(nutritionEndPt, headers=headers, json=nQuery)
    nutrition = nutritionResponse.json()
    #Extract info from request
    for food in nutrition['foods']:
        name = food['food_name']
        cals = round(food['nf_calories'])
        fat = food['nf_saturated_fat']
        photo = food['photo']['highres']

    eQuery = {
        'query':'ran 5 miles',
        'gender':'male',
        'weight_kg':'85',
        'height_cm':'175',
        'age':20
    }
    exerciseResponse = requests.post(exerciseEndPt, headers=headers, json=eQuery)
    exercise = exerciseResponse.json()
    #Extract info from request
    print(exercise)
    for e in exercise['exercises']:
        type = e['user_input']
        burntCals = e['nf_calories']

    #Pass context into template
    context = {'location':(weather['location']['name'] + ", " + weather['location']['country']),
               'condition':weather['current']['condition']['text'],
               'temp':weather['current']['temp_c'],
               'feelslike':weather['current']['feelslike_c'],
               'wind_mph':weather['current']['wind_mph'],
                'wind_dir':windDir,
               'vis':weather['current']['vis_miles'],

               'nName':name,
               'nCals':cals,
               'nFat':fat,
               'nImg':photo,

               'burntCals':burntCals,
               'eType':type
    }
    return render(request, 'homeapp/home.html', context)

#View to register a user
class RegisterUser(CreateView):
    model = User
    form_class = UserCreationWithEmailForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

#View to update User record
@login_required
def updateUser(request):
    context={}
    user = request.user
    form = UserCreationWithEmailForm(request.POST or None, instance = user)
    if form.is_valid():
        #Overwrite existing record
        form.save()
        return redirect('/home')
    context["form"] = form
    return render(request, "registration/updateUser.html", context)

#View to delete User
@login_required
def deleteUser(request):
    context={}
    user = request.user
    if request.method == "POST":
        #Delete record
        user.delete()
        return redirect('/home')
    return render(request, "registration/deleteUser.html", context)


#View to add a workout
@login_required
def addWorkout(request):
    context = {}
    if request.method == 'POST':
        user_id = request.POST['user_id']
        exercise_id = request.POST['exercise_id']
        date = request.POST['date']
        duration = request.POST['duration']
        user = get_object_or_404(User, id=user_id)
        exercise = get_object_or_404(Exercise, id=exercise_id)
        workout = UserWorkouts(user = user, exercise=exercise, date=date, duration=duration)
        workout.save()
        return redirect('/home')
    else:
        return render(request, 'workoutlog/add.html', context)

#View to edit a workout

@login_required
def editWorkout(request, workout_id):
    workout = get_object_or_404(UserWorkouts, id=workout_id)
    if request.method == 'POST':
        date = request.POST['date']
        duration = request.POST['duration']
        workout.date = date
        workout.duration = duration
        workout.save()
        return redirect('/home')
    else:
        return render(request, 'workoutlog/edit.html', {'workout': workout})

#View to delete a workout
@login_required

def deleteWorkout(request, workout_id):
    workout = get_object_or_404(UserWorkouts, id=workout_id)
    if request.method == 'POST':
        workout.delete()
        return redirect('success_page')
    else:
        return render(request, 'workoutlog/delete.html', {'workout': workout})