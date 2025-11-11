from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None  
    email = models.EmailField(unique=True, null=False, blank=False)
    nom = models.CharField(max_length=100, null=True, blank=True)
    prenom = models.CharField(max_length=100, null=True, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=100, null=True, blank=True)
    sex = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=100, null=True, blank=True)
    adresse = models.CharField(max_length=100, null=True, blank=True)
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('proprietaire', 'Proprietaire'),
        ('user', 'Utilisateur'),
        ('locataire', 'Locataire'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='proprietaire')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.nom or ''} {self.prenom or ''}".strip()


# -------------------
# Table des propriétés
# -------------------
class Property(models.Model):
    identifiant = models.CharField(max_length=50, unique=True)
    adresse = models.CharField(max_length=255)
    superficie = models.DecimalField(max_digits=10, decimal_places=2)  # exemple : 125.50 m²
    loyer = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    meublé = models.BooleanField(default=True)
    type = models.CharField(max_length=50)  # ex: Appartement, Maison, Studio, etc.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proprietes")
    image = models.ImageField(upload_to='properties/', null=True, blank=True)

    def __str__(self):
        return f"{self.identifiant} - {self.adresse}"


# -------------------
# Table des locataires
# -------------------
class Locataire(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    mobile = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=150)
    revenu_mensuels = models.DecimalField(max_digits=10, decimal_places=2)
    adresse = models.CharField(max_length=255)
    user_locataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_locataire", null=True)
    proprietaire_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="proprietaire_user" , null=True)


    def __str__(self):
        return f"{self.prenom} {self.nom}"


# -------------------
# Table des locations
# -------------------
class Location(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="locations")
    locataire = models.ForeignKey(Locataire, on_delete=models.CASCADE, related_name="locations")
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    loyer = models.DecimalField(max_digits=10, decimal_places=2)
    garantie = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Location de {self.locataire} - {self.property}"