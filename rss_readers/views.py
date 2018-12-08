from django.shortcuts import render

from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from .models import Feed
from .forms import FeedForm

from bs4 import BeautifulSoup
import re
import requests

def index(request):
	"""Домашняя страница приложения RSS reader"""
	return render(request, 'rss_readers/index.html')

@login_required
def feeds(request):
	"""Выводит список RSS каналов"""
	feeds = Feed.objects.filter(owner=request.user).order_by('date_added')
	context = {'feeds': feeds}
	return render(request, 'rss_readers/feeds.html', context)


class HTML_Items():
	def __init__(self, title, description, href):
		self.title = title
		self.description = description
		self.href = href
		
@login_required
def feed(request, feed_id):
	"""Выводит RSS канал"""
	feed = Feed.objects.get(id=feed_id)
	#Проверка того, что канал принадлежит текущему пользователю
	if feed.owner != request.user:
		raise Http404
	xml = requests.get(feed.link)
	soup = BeautifulSoup(xml.content, 'xml')
	#print(soup.original_encoding)
	#soup = BeautifulSoup(xml.content.decode(soup.original_encoding), 'xml')
	#print(xml.content.decode(soup.original_encoding))

	items_title = [item.title.string for item in soup.find_all('item')]
	items_description = [item.description.string for item in soup.find_all('item')]
	items_link = [item.link.string for item in soup.find_all('item')]

	items_description = list(map(lambda it: re.sub(r'<[^>]*>', '', it), items_description))

	context = {'feed': feed, 'items': [HTML_Items(items_title[i], items_description[i], items_link[i]) for i in range(len(items_description))]}
	return render(request, 'rss_readers/feed.html', context)

@login_required
def new_feed(request):
	"""Определяет новый RSS канал"""
	if request.method != 'POST':
		#Данные не отправились; создаётся новая форма
		form = FeedForm()
	else:
		#Отправлены данные POST; обработать данные
		form = FeedForm(data=request.POST)
		if form.is_valid():
			new_feed = form.save(commit=False)
			new_feed.owner = request.user
			new_feed.save()
			return HttpResponseRedirect(reverse('rss_readers:feeds'))

	context = {'form': form}
	return render(request, 'rss_readers/new_feed.html', context)

@login_required
def edit_feed(request, feed_id):
	"""Редактирует существющий RSS канал"""
	feed = Feed.objects.get(id=feed_id)
	if feed.owner != request.user:
		raise Http404

	if request.method != 'POST':
		#Исходный запрос; форма заполняется данными текущего канала
		form = FeedForm(instance=feed)
	else:
		#Отправка данный POST; обработать данные
		form = FeedForm(instance=feed, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('rss_readers:feed', args=[feed.id]))

	context = {'feed':feed, 'form': form}
	return render(request, 'rss_readers/edit_feed.html', context)
