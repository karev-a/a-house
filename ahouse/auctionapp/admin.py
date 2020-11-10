from django.contrib import admin
from .models import Category, User, AuctionDetails, Bid, BuyNow, AuctionOverview, TransactionAssessment
# Register your models here.

admin.site.register(Category)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(BuyNow)
admin.site.register(AuctionOverview)
admin.site.register(AuctionDetails)
admin.site.register(TransactionAssessment)
