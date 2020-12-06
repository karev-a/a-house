from django.urls import path
from .views import MainPage, SignupPage, ProfileUpdateView, \
    ProfilePageView, AuctionCreateView, \
    AuctionDetailsView, AuctionBidView, AuctionBuyNowView,\
    MyAuctionsView, MyBidsView



urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('signup/', SignupPage.as_view(), name='signup_page'),
    path('profile/<int:pk>/', ProfilePageView.as_view(), name='profile_page'),
    # path('profile/<int:pk>/', ProfileDetailsView.as_view(), name='profile_details'),
    # path('category/', CategoryPageDummy.as_view(), name='category'),
    # path('category/<int:pk>/', CategoryPage.as_view(), name='category_page'),
    path('profile/<int:pk>/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('my_auctions/', MyAuctionsView.as_view(), name='my_auctions'),
    path('my_bids/', MyBidsView.as_view(), name='my_bids'),
    path('auction/', AuctionCreateView.as_view(), name='auction_create'),
    path('auction/<int:pk>/', AuctionDetailsView.as_view(), name='auction_details'),
    path('auction/<int:pk>/bid/', AuctionBidView.as_view(), name='auction_bid'),
    path('auction/<int:pk>/buynow/', AuctionBuyNowView.as_view(), name='auction_buynow'),
]