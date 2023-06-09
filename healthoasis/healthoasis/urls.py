"""healthoasis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
import homeapp, homeapp.views
from homeapp.views import questionnaire_page1, questionnaire_page2, questionnaire_page3, questionnaire_page4

urlpatterns = [
    #Admin URL
    path('admin/', admin.site.urls),

    #Homepage URL
    path('home/', include('homeapp.urls')),
    #Redirect empty URL to home (127.0.0.1:8000/ -> 127.0.0.1:8000/home)
    path('', lambda reuqest: redirect('home/', permanent=False)),
    
    #Nutrition URL
    path('nutrition/', homeapp.views.nutrition, name='nutrition'),
    path('nutrition/search/', homeapp.views.search, name='search'),
    path('nutrition/search/results', homeapp.views.results, name='results'),

    #Chat websocket URLs
    path('chat/', include('chatapp.urls')),

    #Account related URLs:
    
    path('accounts', include('django.contrib.auth.urls')), #Accounts, used to login (accounts/login)
    path('accounts/signup/', homeapp.views.RegisterUser.as_view(), name='signup_user'), #Signup page
    path('accounts/edit/', homeapp.views.updateUser, name="updateUser"),
    path('accounts/delete/', homeapp.views.deleteUser, name="deleteUser"),
    
    #Workout URLs
    path('workoutlog/', homeapp.views.workout2, name='workouts'),
    path('workoutlog/add/', homeapp.views.addWorkout, name='addWorkout'),
    path('workoutlog/edit/<int:wid>/', homeapp.views.editWorkout, name='editWorkout'),
    path('workoutlog/delete/<int:wid>/', homeapp.views.deleteWorkout, name='deleteWorkout'),
    
    #Exercise URLs
    path('workoutlog/search/', homeapp.views.exerciseSearch, name='exerciseSearch'),
    path('workoutlog/search/results', homeapp.views.exerciseResults, name='exerciseResults'),

    #Progress URLs
    path('progress/', homeapp.views.progress, name='progress'),

    #about URL
    path('home/about', homeapp.views.about , name='about'),

    #Nutrition URLs pertaining to users.
    path('nutrition/log', homeapp.views.logUserNutrition, name = 'nutritionLog'),

    #Questionnaire URLs
    path('questionnaire/page1/', questionnaire_page1, name='questionnaire_page1'),
    path('questionnaire/page2/', questionnaire_page2, name='questionnaire_page2'),
    path('questionnaire/page3/', questionnaire_page3, name='questionnaire_page3'),
    path('questionnaire/page4/', questionnaire_page4, name='questionnaire_page4'),
]
