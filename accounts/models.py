from django.db import models
from django.contrib.auth.models import User
from django.forms import DateField
from JobRecommenderSystem import settings


class signupModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dateofbirth = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    skills = models.TextField(null=True)
    interests = models.TextField(null=True)
    objectivestatement = models.CharField(max_length=100)
    idformongo = models.TextField(null=True)


class workexperienceModel(models.Model):
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    startDate = models.CharField(max_length=100)
    endDate = models.CharField(max_length=100)
    UserExperience = models.ForeignKey(signupModel, on_delete=models.CASCADE)


class Education(models.Model):
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    startdateedu = models.CharField(max_length=100)
    enddateedu = models.CharField(max_length=100)
    UserEducation = models.ForeignKey(signupModel, on_delete=models.CASCADE)
