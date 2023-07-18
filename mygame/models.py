from django.db import models
from django.contrib.auth.models import User

class Matrix(models.Model):

    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
 
class Cell(models.Model):

    matrix = models.ForeignKey(Matrix,on_delete=models.CASCADE)
    row = models.IntegerField()
    col = models.IntegerField()
    val = models.IntegerField()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matrix = models.ForeignKey(Matrix, on_delete=models.SET_NULL, null=True)


