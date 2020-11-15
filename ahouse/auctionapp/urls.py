from django.urls import path
from .views import TestPage, SignupPage, ProfileUpdateView, ProfileDetailsView


urlpatterns = [
    path('', TestPage.as_view(), name='test_page'),
    path('signup/', SignupPage.as_view(), name='signup_page'),
    path('profile/', TestPage.as_view(), name='profile_page'),
    path('profile/<int:pk>/', ProfileDetailsView.as_view(), name='profile_details'),
    path('profile/<int:pk>/update/', ProfileUpdateView.as_view(), name='profile_update'),
]