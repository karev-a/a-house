from django.urls import path
from .views import MainPage, SignupPage, ProfileUpdateView, ProfileDetailsView, AuctionCreateView, ProfilePageView


urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('signup/', SignupPage.as_view(), name='signup_page'),
    path('profile/', ProfilePageView.as_view(), name='profile_page'),
    path('profile/<int:pk>/', ProfileDetailsView.as_view(), name='profile_details'),
    path('profile/<int:pk>/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('auction/', AuctionCreateView.as_view(), name='auction_create'),
]