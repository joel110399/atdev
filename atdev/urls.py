from django.urls import path

from calculator import views as calculator_views

urlpatterns = [
    path('', calculator_views.home, name='home'),
]
