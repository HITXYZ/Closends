import json
from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

def friend_index(request, friend):
    return render(request, 'closends/friend_index.html')