from django.urls import path
from . import views

app_name = 'lists'
urlpatterns = [
	#ex: /lists/
	path('', views.HomePageView, name='home'),
	
]