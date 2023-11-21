from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.forms import model_to_dict
from .models import Doctor, Patient
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
import json
# Create your views here.

def signup(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        uname = data.get('username')
        pword = data.get('password')
        user = authenticate(username=uname, password=pword)
        if user.IsAuthenticated and data.get('role') == 'Doctor':
            user = Doctor.objects.create(
                username=uname,
                password=pword,
                role=data.get('role')
            )
            user.save()
            dct_obj = model_to_dict(user)
            js = json.dumps(dct_obj)
            return JsonResponse(js, safe=False)
        elif user.is_authenticated and data.get('role') == 'Patient':
            return JsonResponse({'message': 'Unauthorized'})
        
def u_login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        uname = data.get('username')
        pword = data.get('password')
        user = authenticate(username=uname, password=pword)
        if user.IsAuthenticated:
            login(uname, pword)
            return JsonResponse({'message': 'ok'})