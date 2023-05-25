from django.urls import path,include
from . views import *
urlpatterns = [
    path('', gpt,name="gpt"),
]