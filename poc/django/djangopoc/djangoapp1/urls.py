from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

# Map the views functions to urls
urlpatterns = [
    path('', views.greet, name='home')  # Home Page
]