from django.urls import path, include
from .views import TestPage


urlpatterns = [
    path('', TestPage.as_view(), name='test_page'),
]