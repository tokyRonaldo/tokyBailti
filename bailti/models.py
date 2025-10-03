from django.db import models

# Create your models here.
class User(models.Model):
    email=models.EmailField()
    nom=models.CharField(max_length=100)
    prenom=models.CharField(max_length=100)
    date_naissance=models.DateField()
    lieu_naissance=models.CharField(max_length=100)
    sex=models.CharField(max_length=20)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.nom