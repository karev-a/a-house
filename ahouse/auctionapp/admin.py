from django.contrib import admin
from .models import Category, Profile, Auction, Bid, BuyNow, AuctionOverview, TransactionAssessment
# Register your models here.

admin.site.register(Category)
admin.site.register(Profile)
admin.site.register(Bid)
admin.site.register(BuyNow)
admin.site.register(AuctionOverview)
admin.site.register(TransactionAssessment)


class AuctionAdmin(admin.ModelAdmin):
    readonly_fields = ('auction_start',)

admin.site.register(Auction, AuctionAdmin)
