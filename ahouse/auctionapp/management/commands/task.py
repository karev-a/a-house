from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from auctionapp.models import Auction
import time


class Command(BaseCommand):
    help = 'Update Auction Status'

    def handle(self, *args, **options):
        while True:
            auctions = Auction.objects.filter(auction_active=True)
            for auction in auctions:
                if auction.auction_end > timezone.datetime.now():
                    pass
                else:
                    auction.auction_active = False
                    auction.save()
                time.sleep(1)
