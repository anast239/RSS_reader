"""Определяет схемы URL для rss_readers"""

from django.conf.urls import url

from . import views

urlpatterns = [
	#Домашняя страница
	url(r'^$', views.index, name='index'),

	#Вывод всех каналов
	url(r'^feeds/$', views.feeds, name='feeds'),

	#Cтраница с RSS каналом
	url(r'^feeds/(?P<feed_id>\d+)/$', views.feed, name='feed'),

	#Страница для добавления нового RSS канала
	url(r'^new_feed/$', views.new_feed, name='new_feed'),

	#Страница для редактирования RSS канала
	url(r'^edit_feed/(?P<feed_id>\d+)/$', views.edit_feed, name='edit_feed'),

	
]