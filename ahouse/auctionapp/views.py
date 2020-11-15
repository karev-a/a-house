from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Profile
from .forms import SignupForm
from django.urls import reverse_lazy


# Create your views here.


class TestPage(ListView):
    model = Profile
    template_name = "test_page.html"
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["page_title"] = "Test page"
        return context


class SignupPage(CreateView):
    template_name = 'signup_page.html'
    form_class = SignupForm
    success_url = reverse_lazy('test_page')

class ProfileDetailsView(DetailView):
    model = Profile
    template_name = "profile_details.html"
    context_object_name = 'profile'
    success_url = reverse_lazy('profile_page')

class ProfileUpdateView(UpdateView):
    model = Profile
    template_name = 'profile_update.html'
    context_object_name = 'profile'
    fields = ['phone_number', 'address', 'town','post_code','country','avatar']
    success_url = reverse_lazy('profile_page')






