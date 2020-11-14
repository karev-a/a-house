from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile


# Create your views here.


class TestPage(ListView):
    model = Profile
    template_name = "test_page.html"
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["page_title"] = "Test page"
        return context



