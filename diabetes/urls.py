from django.urls import path
from . import views
app_name = 'diabetes'
urlpatterns = [
    path('', views.get_recommendations, name='index'),
    ]