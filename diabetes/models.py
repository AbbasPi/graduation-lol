from django.contrib.auth.models import User
from django.db import models


class GenderChoices(models.TextChoices):
    male = 'Male', 'Male'
    female = 'Female', 'Female'


class DiabetesTypeChoices(models.TextChoices):
    type_1 = 'Type 1', 'Type 1'
    type_2 = 'Type 2', 'Type 2'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    diabetes_type = models.CharField(max_length=20, default=DiabetesTypeChoices.type_2,choices=DiabetesTypeChoices.choices)
    pregnancy_status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class GlucoseData(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    glucose_level = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_profile.user.username} - {self.glucose_level} mg/dL - {self.timestamp}'
