from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate,login,logout
from parking.models import *
from django.core import serializers
from django.shortcuts import HttpResponse
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from datetime import datetime
from datetime import timedelta
import cv2
import json

@require_http_methods(['GET'])
@csrf_exempt
def park_view(request):
    if request.method == 'GET':
        data={}

        uid=request.GET.get('uid')
        pname=request.GET.get('pname')
        status='parked'

        obj = Park.objects.get(pid=pname)
        if obj.status == 'parked':
            data['status'] = 'error'
        else :
            obj.uid = uid
            obj.status = 'parked'
            obj.save()
            data['status']=str(obj.status)
        
        park = Park.objects.all()
        img = cv2.imread("/home/ahmed/parking.png")
        for p in park:
            if p.status == 'left':
                img=cv2.circle(img,(p.pos_x,p.pos_y),10,(0,255,0),-1)
            else:
                img=cv2.circle(img,(p.pos_x,p.pos_y),10,(0,0,255),-1)

        cv2.imwrite("/home/ahmed/parking2.png",img)
        with open("/home/ahmed/parking2.png", "rb") as f:
            return HttpResponse(f.read(), content_type="image/bmp")

@require_http_methods(['GET'])
@csrf_exempt
def leave_view(request):
    if request.method == 'GET':
        data={}

        uid=request.GET.get('uid')
        obj = Park.objects.get(uid=uid)
        if obj.status == 'left':
            data['status'] = 'error'
        else :
            obj.uid = 0
            obj.status = 'left'
            obj.save()
            data['status']=str(obj.status)
        
        park = Park.objects.all()
        img = cv2.imread("/home/ahmed/parking.png")
        for p in park:
            if p.status == 'left':
                img=cv2.circle(img,(p.pos_x,p.pos_y),10,(0,255,0),-1)
            else:
                img=cv2.circle(img,(p.pos_x,p.pos_y),10,(0,0,255),-1)

        cv2.imwrite("/home/ahmed/parking2.png",img)
        with open("/home/ahmed/parking2.png", "rb") as f:
            return HttpResponse(f.read(), content_type="image/bmp")

@require_http_methods(['GET'])
@csrf_exempt
def parking_image(req):
    if req.method=='GET':
        park = Park.objects.all()
        img = cv2.imread("/home/ahmed/parking.png")
        for p in park:
            if p.status == 'left':
                img=cv2.circle(img,(p.pos_x,p.pos_y),10,(0,255,0),-1)
            else:
                img=cv2.circle(img,(p.pos_x,p.pos_y),10,(0,0,255),-1)

        cv2.imwrite("/home/ahmed/parking2.png",img)
        with open("/home/ahmed/parking2.png", "rb") as f:
            return HttpResponse(f.read(), content_type="image/bmp")

@require_http_methods(['GET'])
@csrf_exempt
def locate_car(request):
    if request.method == 'GET':
        data={}
        uid=request.GET.get('uid')

        obj = Park.objects.get(uid=uid)
        if obj.status == 'left':
            data['status'] = 'error'
        else :
            data['status']=str(obj.status)
        
        park = Park.objects.all()
        img = cv2.imread("/home/ahmed/parking.png")
        for p in park:
            print(uid,p.uid)
            if p.status == 'left':
                img=cv2.circle(img,(p.pos_x,p.pos_y),10,(0,255,0),-1)
            elif p.uid == int(uid):
                img=cv2.circle(img,(p.pos_x,p.pos_y),10,(0,255,255),-1)
            else:
                img=cv2.circle(img,(p.pos_x,p.pos_y),10,(0,0,255),-1)

        cv2.imwrite("/home/ahmed/parking2.png",img)
        with open("/home/ahmed/parking2.png", "rb") as f:
            return HttpResponse(f.read(), content_type="image/bmp")
