from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView
from .models import Profile, User, Auction, Category, AuctionOverview, Bid, BuyNow
from .forms import SignupForm, AuctionCreateForm, BidForm, BuyNowForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, request
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.db.models import Q
from  django.shortcuts import get_object_or_404



# Create your views here.


class MainPage(ListView):
    model = Auction
    template_name = 'auctions_main.html'
    context_object_name = 'auctions'
    ordering = 'main_page'

    def get_queryset(self):
        auctions_filter = self.request.GET.get('filter_by')
        category_filter = self.request.GET.get('category')
        order = self.request.GET.get('ordering', 'auction_start')
        auctions = Auction.objects.all()
        if category_filter and category_filter != 'all':
            auctions = auctions.filter(category__pk=category_filter)
        auctions = auctions.order_by(order)
        if auctions_filter:
            auctions = auctions.filter(Q(title__icontains=auctions_filter) | Q(description__icontains=auctions_filter))
        return auctions

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['category'] = self.request.GET.get('category')
        context['orderby'] = self.request.GET.get('ordering', 'auction_start')
        context['auctions_filter'] = self.request.GET.get('auctions_filter')
        return context


class SignupPage(CreateView):
    template_name = 'signup_page.html'
    form_class = SignupForm
    success_url = reverse_lazy('main_page')


class ProfilePageView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profile_details.html'
    context_object_name = 'profile'
    success_url = reverse_lazy('main_page')

    def check_user(self):
        current_user = super(ProfilePageView, self).get_object()
        if current_user.user != self.request.user:
            raise PermissionDenied()
        return current_user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'profile_update.html'
    context_object_name = 'profile'
    fields = ['phone_number', 'address', 'town', 'post_code', 'country', 'avatar']
    success_url = reverse_lazy('main_page')

    def check_user(self):
        current_user = super(ProfileUpdateView, self).get_object()
        if current_user.user != self.request.user:
            raise PermissionDenied()
        return current_user


class AuctionCreateView(LoginRequiredMixin, CreateView):
    form_class = AuctionCreateForm
    template_name = 'auction_create.html'
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        auction = form.save(commit=False)
        auction.user = self.request.user.profile
        auction.save()
        return super(AuctionCreateView, self).form_valid(form)


class AuctionDetailsView(DetailView):
    model = Auction
    template_name = 'auction_details.html'
    context_object_name = 'auction'
    success_url = reverse_lazy('main_page')

    def get_object(self):
        view_count = super().get_object()
        view_count.views_count += 1
        view_count.save()
        return view_count

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['auction_details'] = Auction.objects.get(pk=self.kwargs.get('pk'))
        return context


class AuctionBidView(LoginRequiredMixin, CreateView):
    form_class = BidForm
    template_name = 'auction_bid.html'
    success_url = reverse_lazy('main_page')
    context_object_name = 'bid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['auction_details'] = Auction.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        bid = form.save(commit=False)
        bid.user = self.request.user.profile
        bid.auction = Auction.objects.get(pk=self.kwargs.get('pk'))
        bid.bid_time = timezone.datetime.now()
        if bid.auction.user == bid.user:
            return HttpResponse('no bids on your own items!')
        if bid.auction.min_bid > bid.bid:
            return HttpResponse('u bid too low')
        if bid.bid_time > bid.auction.auction_end:
            return HttpResponse('this auction has expired')
        if bid.auction.final_bid >= bid.bid:
            return HttpResponse('u bid too low')
        bid.auction.final_bid = bid.bid
        bid.auction.save()
        form.save()
        return super(AuctionBidView, self).form_valid(form)


class AuctionBuyNowView(LoginRequiredMixin, CreateView):
    form_class = BuyNowForm
    template_name = 'auction_buynow.html'
    success_url = reverse_lazy('main_page')
    context_object_name = 'bid'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['auction_details'] = Auction.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        bid = form.save(commit=False)
        bid.user = self.request.user.profile
        bid.auction = Auction.objects.get(pk=self.kwargs.get('pk'))
        bid.bid_time = timezone.datetime.now()
        bid.bid = bid.auction.max_bid
        if bid.auction.user == bid.user:
            return HttpResponse('no buys for your own items!')
        if bid.auction.auction_active is False:
            return HttpResponse('this auction is over!')
        if bid.bid_time > bid.auction.auction_end:
            return HttpResponse('this auction has expired')
        bid.auction.final_bid = bid.bid
        bid.auction.auction_active = False
        bid.auction.save()
        form.save()
        return super(AuctionBuyNowView, self).form_valid(form)


class MyAuctionsView(LoginRequiredMixin, ListView):
    model = Auction
    template_name = 'my_auctions.html'
    context_object_name = 'auction'
    success_url = reverse_lazy('main_page')

    def check_user(self):
        current_user = super(MyAuctionsView, self).get_object()
        if current_user.user != self.request.user:
            raise PermissionDenied()
        return current_user

    def get_queryset(self):
        queryset = Auction.objects.filter(user=self.request.user.profile)
        return queryset

    def get_context_data(self):
        context = super(MyAuctionsView, self).get_context_data()
        context['queryset'] = self.get_queryset()
        context['auction'] = Auction.objects.all()
        return context


class MyBidsView(LoginRequiredMixin, ListView):
    model = Bid
    template_name = 'my_bids.html'
    context_object_name = 'bid'
    success_url = reverse_lazy('main_page')

    def check_user(self):
        current_user = super(MyBidsView, self).get_object()
        if current_user.user != self.request.user:
            raise PermissionDenied()
        return current_user

    def get_queryset(self):
        queryset = Bid.objects.filter(user=self.request.user.profile)
        return queryset

    def get_context_data(self):
        context = super(MyBidsView, self).get_context_data()
        context['queryset'] = self.get_queryset()
        context['bid'] = Bid.objects.all()
        return context

class MyBuyOutsView(LoginRequiredMixin, ListView):
    model = BuyNow
    template_name = 'my_purchases.html'
    context_object_name = 'bid'
    success_url = reverse_lazy('main_page')

    def check_user(self):
        current_user = super(MyBuyOutsView, self).get_object()
        if current_user.user != self.request.user:
            raise PermissionDenied()
        return current_user

    def get_queryset(self):
        queryset = BuyNow.objects.filter(user=self.request.user.profile)
        return queryset

    def get_context_data(self):
        context = super(MyBuyOutsView, self).get_context_data()
        context['queryset'] = self.get_queryset()
        context['bid'] = BuyNow.objects.all()
        return context