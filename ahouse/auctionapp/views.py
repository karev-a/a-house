from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView, TemplateView
from .models import Profile, User, Auction, Category, AuctionOverview, Bid
from .forms import SignupForm, AuctionCreateForm, BidForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django import forms
from django.utils import timezone
from django.shortcuts import get_object_or_404


# Create your views here.


class MainPage(ListView):
    model = AuctionOverview
    template_name = 'auctions_main.html'
    context_object_name = 'auctions'

    def get_queryset(self):
        return Auction.objects.filter().order_by('views_count')


class SignupPage(CreateView):
    template_name = 'signup_page.html'
    form_class = SignupForm
    success_url = reverse_lazy('main_page')


class ProfilePageView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profile_page.html'
    context_object_name = 'profile'
    success_url = reverse_lazy('main_page')

    def check_user(self):
        current_user = super(ProfilePageView, self).get_object()
        if current_user.user != self.request.user:
            raise PermissionDenied()
        return current_user


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profile_details.html'
    context_object_name = 'profile'
    success_url = reverse_lazy('main_page')

    def check_user(self):
        current_user = super(ProfileDetailsView, self).get_object()
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
            return HttpResponse('this auction as expired')
        if bid.auction.final_bid >= bid.bid:
            return HttpResponse('u bid too low')
        else:
            bid.auction.final_bid = bid.bid
            bid.auction.save()
        form.save()
        return super(AuctionBidView, self).form_valid(form)
