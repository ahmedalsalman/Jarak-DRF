from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from hashlib import md5

class Product(models.Model):
	name = models.CharField(max_length=150)
	description = models.TextField(null=True, blank=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	image = models.TextField(null=True, blank=True)
	available = models.BooleanField(default = True)


	def __str__(self):
		return self.name

class RentedItem(models.Model):
	tenant = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
	product = models.OneToOneField(Product,on_delete=models.CASCADE)
	date = models.DateTimeField(default=datetime.now())
	rented = models.BooleanField(default = True) #might change this to charFiled with choices (rented, unrented, on queue)


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
	def avatar(self, size):
		digest = md5(self.user.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


	def __str__(self):
		return str(self.user.username)

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)