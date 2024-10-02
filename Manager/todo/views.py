from typing import List
from django.core.checks import messages
from django.shortcuts import render, redirect
from .models import TodoTasks
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


# Create your views here.
