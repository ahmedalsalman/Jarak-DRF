from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from hashlib import md5

# This model is not used yet but we will be using it in the future as to categorize items by location
class Location(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    image=models.TextField(null=True, blank=True)

    def avatar(self, size):
        # This is not used yet but we want to have it as to be able to upload the profile image of the user instead of having a default one by Gravatar
        if(self.image is None): 
            digest = md5(self.user.email.lower().encode('utf-8')).hexdigest()
            return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
        else:
            return self.image
    def __str__(self):
        return self.user.username


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name="renting")
    image = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name

    def rented_by(self):
        history = self.history.all()
        if history.exists():
            tenant = history.last().tenant
            if history.last().end_datetime is None:
                return tenant.id
        return None


class RentedItem(models.Model):
    tenant = models.ForeignKey( Profile, on_delete=models.CASCADE, null=True, blank=True, related_name="history")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="history")
    start_datetime = models.DateTimeField(auto_now_add=True, null=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    