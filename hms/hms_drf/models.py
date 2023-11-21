from django.db import models
from django_extensions.db.models import (
    TimeStampedModel,
    ActivatorModel,
    TitleSlugDescriptionModel
)
from django.contrib.auth import (authenticate,  models as Models)
# Create your models here.

class Doctor(Models.User):
    name = models.CharField()

class Patient(Models.User):
    name = models.CharField


class Appointment(models.Model, TimeStampedModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    
