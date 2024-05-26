from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.model_home, name='model_home'),
    path('main', include('main.urls')),
    path('results', views.show_results, name='results'),
] 