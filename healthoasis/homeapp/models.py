from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, time
from django.utils import timezone




#Model to create a User table to allow us to store required User information in the database.
class UserDetails(models.Model): 
    email =  models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    gender = models.CharField(max_length=10)
    bmi = models.FloatField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.username

#Model to create a UserReport table to store reports for the User generated by the application.
class UserReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_date = models.DateField(auto_now_add=True)
    report_data = models.JSONField()

def __str__(self):
    return f"Report for {self.user.username} on {self.report_date}"

#Model to create a UserActivity table to store information on whether the User is active or not
#and over a period of time if needed.
class UserActivity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - { 'Active' if self.active else 'Inactive'}"

#Model to create an ExerciseType table to store information on the different type of exercises
#available to be done by the User.
class ExerciseType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

#Model to create an Exercise table to store information on the different exercises avaiable within
#each exercise type.
class Exercise(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

#Model to create a Workout table to store information about each workout.
class Workout(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateField(null=True)
    time = models.TimeField(default=time(0, 0))
    exercises = models.ManyToManyField(Exercise, default=10)

    def __str__(self):
        return self.name

#Model to create a UserWorkouts table to store information on the workouts relating to the Users.
class UserWorkouts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    duration = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.workout.name} ({self.date})"

#Model to create a UserNutrition table to store information of the caloric intake of the User.
class UserNutrition(models.Model):
    calories = models.FloatField(validators=[MinValueValidator(0.0)])
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=True, unique = True)
    last_updated = models.DateTimeField(auto_now = True)

    def time_since_creation(self):
        now = timezone.now()
        timedelta = now - self.last_updated
        return timedelta.days
    
    def __str__(self):
        return str(self.calories) +  " " + str(self.user) + " " + str(self.last_updated)


class BreakfastOption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.CharField(max_length=100)
    health_level = models.CharField(max_length=20)