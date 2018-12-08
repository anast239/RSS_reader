from django.db import models
from django.contrib.auth.models import User

class Feed(models.Model):
	"""RRS канал, который добавляет пользователь"""
	title = models.CharField(max_length=200)
	link = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)
	category = models.CharField(max_length=200)
	owner = models.ForeignKey(User)

	def __str__(self):
		"""Возвращает строковое представление модели"""
		return self.title
