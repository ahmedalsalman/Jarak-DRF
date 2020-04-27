from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save


class Product(models.Model):
	name = models.CharField(max_length=150)
	description = models.TextField(null=True, blank=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	image = models.TextField(null=True, blank=True)
	available = models.BooleanField(default = True)


	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Product"

class Profile(models.Model):
	Abdali = 'Abdali'
	Arjan = 'Arjan'
	Tabarbour = 'Tabarbour'
	Wadi_el_seir = 'Wadi_el_seir'
	Aein_Al_Basha = 'Aein_Al_Basha'
	REGIONS = [
		(Abdali, 'Abdali'),
		(Arjan, 'Arjan'),
		(Tabarbour, 'Tabarbour'),
		(Wadi_el_seir, 'Wadi_el_seir'),
		(Aein_Al_Basha, 'Aein_Al_Basha'),
	]
	user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="profile")
	location = models.CharField(max_length=25, choices=REGIONS, default=Abdali)
	avatar = models.TextField(null=True, blank=True)


	def __str__(self):
		return str(self.user.username)        
