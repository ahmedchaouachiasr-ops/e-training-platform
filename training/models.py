from django.db import models
from jsonschema import ValidationError

# Create your models here.

class Formateur(models.Model):
    nom = models.CharField(max_length=90)
    email = models.EmailField()
    
    
    def __str__(self):
        return f"Mr. {self.nom}"      # pour afficher le nom du formateur dans l'interface admin
    

class Apprenant(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    def __str__(self):
        return self.nom


class Cours(models.Model):
    
    titre= models.CharField(max_length=150)
    description = models.TextField()
    duree = models.IntegerField()
    published = models.BooleanField(default=False)
    formateur = models.ForeignKey(Formateur, on_delete=models.CASCADE)
    apprenants = models.ManyToManyField(Apprenant)

    def clean(self):
        if self.duree <=0:
            raise ValidationError(" La durée doit être supérieur à 0")
        
    def  __str__(self):
        return f" {self.titre} -- {self.formateur} "
    