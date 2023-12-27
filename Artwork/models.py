from django.db import models
from django.contrib.auth.models import User
import uuid


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=80, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="profile/")
    url = models.URLField(null=True, blank=True)
    id = models.UUIDField(primary_key=True, unique=True,
                          default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.user.username if self.user else 'Profile without User'


class Artwork(models.Model):
    proprietaire = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True
    )

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    title = models.CharField(max_length=100)
    body = models.TextField()
    image = models.URLField()
    price = models.FloatField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class DemandePret(models.Model):
    id_demande_pret = models.AutoField(primary_key=True)
    artwork = models.ForeignKey(
        Artwork, on_delete=models.CASCADE, null=True, default=None)
    date_debut = models.DateField(null=True)
    h_debut = models.TimeField(null=True)
    date_fin = models.DateField(null=True)
    h_fin = models.TimeField(null=True)
    pj_demande = models.FileField(upload_to='uploads/', null=True, blank=True)
    acquereur = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        verbose_name = 'Demande Pret'
        verbose_name_plural = 'Demandes Prets'
