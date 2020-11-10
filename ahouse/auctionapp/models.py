from django.db import models


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to='images/logos', blank=True)

    def __str__(self):
        return "Category: " + self.name


class User(models.Model):
    ACCSTATUS = (
        ('ACT', 'Active'),
        ('INA', 'Inactive'),
        ('BLK', 'Blocked')
    )

    ACCTYPES = (
        ('PRE', 'Premium'),
        ('Nor', 'Normal')
    )
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    phone_number = models.CharField(max_length=25)
    address = models.CharField(max_length=255)
    town = models.CharField(max_length=45)
    post_code = models.CharField(max_length=25)
    country = models.CharField(max_length=45)
    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=25)
    login_email = models.EmailField(unique=True)
    balance = models.DecimalField(max_digits=6, decimal_places=2)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    account_status = models.CharField(max_length=25, choices=ACCSTATUS)
    avatar = models.ImageField(upload_to='images/avatars', blank=True)
    account_type = models.CharField(max_length=25, choices=ACCTYPES)


class AuctionDetails(models.Model):
    PROMOTION = (
        ('PRO', 'Promoted'),
        ('COM', 'Common')
    )

    title = models.CharField(max_length=55)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/items', blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, null=True, blank=True)
    min_bid = models.FloatField()
    max_bid = models.FloatField()
    final_bid = models.FloatField()
    promoted = models.CharField(max_length=25, choices=PROMOTION)
    location = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    auction_start = models.DateTimeField(auto_now_add=True, editable=False)
    auction_end = models.DateTimeField()
    views_count = models.PositiveIntegerField(default=0)


class Bid(models.Model):
    auction_id = models.ForeignKey(AuctionDetails, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_time = models.DateTimeField()
    bid = models.FloatField()


class BuyNow(models.Model):
    auction_id = models.ForeignKey(AuctionDetails, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_time = models.DateTimeField()
    bid = models.FloatField()


class AuctionOverview(models.Model):
    auction_id = models.ForeignKey(AuctionDetails, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class TransactionAssessment(models.Model):
    RATINGS = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    )

    purchase = models.ForeignKey(AuctionDetails, on_delete=models.CASCADE)
    seller_rating = models.CharField(max_length=1, choices=RATINGS)
    seller_comment = models.CharField(max_length=255)
    buyer_rating = models.CharField(max_length=1, choices=RATINGS)
    buyer_comment = models.CharField(max_length=255)
