from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Auction, Bid, BuyNow
from django.utils import timezone


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("This email is already in use!")
        return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AuctionCreateForm(forms.ModelForm):
    day_one = timezone.now() + timezone.timedelta(hours=24)
    day_three = timezone.now() + timezone.timedelta(hours=72)
    day_seven = timezone.now() + timezone.timedelta(hours=168)

    AUCTION_LENGTH = (
        (day_one, '1 day'),
        (day_three, '3 days'),
        (day_seven, '7 days')
    )

    auction_end = forms.DateTimeField(input_formats=['m.d.Y H:i'], widget=forms.Select(choices=AUCTION_LENGTH))

    class Meta:
        model = Auction
        fields = ('title', 'description', 'image', 'category', 'min_bid', 'max_bid', 'promoted', 'auction_end')


class BidForm(forms.ModelForm):
    bid = forms.FloatField()
    class Meta:
        model = Bid
        fields = ('bid',)

class BuyNowForm(forms.ModelForm):

    class Meta:
        model = BuyNow
        fields = ()
        # exclude = ('bid',)
