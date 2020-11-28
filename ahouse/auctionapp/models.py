from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .countries_list import CTRCHOICES
from django.utils import timezone

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to='images/logos', blank=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    ACCTYPES = (
        ('PRE', 'Premium'),
        ('Nor', 'Normal')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=25)
    address = models.CharField(max_length=255)
    town = models.CharField(max_length=45)
    post_code = models.CharField(max_length=25)
    country = models.CharField(max_length=45, choices=CTRCHOICES)
    balance = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    account_type = models.CharField(max_length=25, choices=ACCTYPES)
    avatar = models.ImageField(upload_to='images/avatars', blank=True)

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    def __str__(self):
        return self.user.username



class Auction(models.Model):
    PROMOTION = (
        ('PRO', 'Promoted'),
        ('COM', 'Common')
    )
    user = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, null=True, blank=True)
    title = models.CharField(max_length=55)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/items', blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True)
    min_bid = models.FloatField()
    max_bid = models.FloatField()
    final_bid = models.FloatField()
    promoted = models.CharField(max_length=25, choices=PROMOTION)
    auction_start = models.DateTimeField(auto_now_add=True, editable=False)
    auction_end = models.DateTimeField()
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    bid_time = models.DateTimeField()
    bid = models.FloatField()

    def __str__(self):
        return f"{self.auction} - {self.user} - {self.bid}"


class BuyNow(models.Model):
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    bid_time = models.DateTimeField()
    bid = models.FloatField()


class AuctionOverview(models.Model):
    auction_id = models.ForeignKey(Auction, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)


class TransactionAssessment(models.Model):
    RATINGS = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )

    purchase = models.ForeignKey(Auction, on_delete=models.CASCADE)
    seller_rating = models.CharField(max_length=1, choices=RATINGS)
    seller_comment = models.CharField(max_length=255)
    buyer_rating = models.CharField(max_length=1, choices=RATINGS)
    buyer_comment = models.CharField(max_length=255)
