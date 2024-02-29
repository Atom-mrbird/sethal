from django.contrib.auth.forms import UserCreationForm
from django.db.migrations import serializer
from django.urls import reverse_lazy
from django.views import generic
from rest_framework import response, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CardInformationSerializer
import stripe

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
