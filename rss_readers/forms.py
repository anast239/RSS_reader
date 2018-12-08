from django import forms

from .models import Feed

class FeedForm(forms.ModelForm):
	class Meta:
		model = Feed
		fields = ['title', 'link', 'category']
		labels = {'title': 'Title', 'link': 'RSS feed', 'category': 'Category'}
