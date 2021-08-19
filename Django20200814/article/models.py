from django.db import models

# Create your models here.
from user.models import User


class Article(models.Model):
    article = models.ForeignKey(to=User,on_delete=models.CASCADE)

