from django.db import models

# Create your models here.
from govtech_csg_xcg.securemodelpkid.model import RandomIDModel


class Customer(models.Model):
    name = models.CharField(max_length=50)


class CustomerWithRandomID(RandomIDModel):
    name = models.CharField(max_length=50)
