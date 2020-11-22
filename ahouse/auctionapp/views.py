from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Profile, User, Auction
from .forms import SignupForm, AuctionCreateForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.core.exceptions import PermissionDenied
from django import forms


# Create your views here.


class MainPage(ListView):
    model = Auction
    template_name = 'auctions_main.html'
    context_object_name = 'auctions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["page_title"] = "Main page"
        return context


class SignupPage(CreateView):
    template_name = 'signup_page.html'
    form_class = SignupForm
    success_url = reverse_lazy('main_page')


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


class AuctionCreateView(CreateView):
    form_class = AuctionCreateForm
    template_name = 'auction_create.html'
    success_url = reverse_lazy('main_page')
