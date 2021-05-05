from django.db import models

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class Event(models.Model):
	name = models.CharField(max_length=256, blank=False, null=False, default='(empty)')
	attendants = models.ManyToManyField(User)
	starting_at = models.DateTimeField(auto_now=False, auto_now_add=False)
	password = models.CharField(max_length=512, blank=True, null=True)

	__old_pwd = None

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__old_pwd = self.password

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if (self.__old_pwd != self.password or not self.pk) and self.password:
			self.password = make_password(self.password)
		super().save(*args, **kwargs)