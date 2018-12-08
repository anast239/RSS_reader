from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm

def logout_view(request):
	"""Завершает сеанс работы с приложением"""
	logout(request)
	return HttpResponseRedirect(reverse('rss_readers:index'))

def register(request):
	"""Pегистрирует нового пользователя"""
	if request.method != 'POST':
		#Отобразить пустую форму регистрации
		form = UserCreationForm()
	else:
		#Обработка заполненной формы
		form = UserCreationForm(data=request.POST)

		if form.is_valid():
			new_user = form.save()
			#Выполнение входа и перенапраление на домашнюю страницу
			authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
			login(request, authenticated_user)
			return HttpResponseRedirect(reverse('rss_readers:index'))
	context = {'form': form}
	return render(request, 'users/register.html', context)

