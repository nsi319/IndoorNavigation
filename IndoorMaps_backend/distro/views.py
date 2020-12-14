from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate,login,logout
from distro.models import *
from django.core import serializers
from django.shortcuts import HttpResponse
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from datetime import datetime
from datetime import timedelta
import json
import math
import matplotlib.pyplot as plt
import cv2
import os
import random


dict1={
    '7-8':0,
    '8-9':0,
    '9-10':0,
    '10-11':0,
    '11-12':0,
    '12-13':0,
    '13-14':0,
    '14-15':0,
    '15-16':0,
    '16-17':0,
    '17-18':0,
    '18-19':0,
    '19-20':0,
    '20-21':0   
}
dict2={
    '1':0,
    '2':0,
    '3':0,
    '4':0,
    '5':0,
    '6':0,
    '7':0,
    '8':0,
    '9':0,
    '10':0,
    '11':0,
    '12':0,
    '13':0,
    '14':0   
}

rp_list=["hack_room","stage","dining","exit","regdesk","room1","room2","mentor_room","game_room"]
   
@require_http_methods(['POST'])
@csrf_exempt
def entry(request):
    if request.method == 'POST':
        data={}
        print(request.body)
        body = json.loads(request.body)
        starttime= body['start_time']
        end_time=body['end_time']
        rname=body['rname']
        userid = body['userid'] 
        tmp=Dist.objects.create(rp=rname, uid=userid,exits=end_time,enters=starttime)

        if tmp is not None:
            data['status']='succes'
        else:
            data['status'] = 'error'
        # for i in range(1,4):
        #     for j in range(9):
        #         now = datetime.now()+timedelta(minutes=i*j*2)-timedelta(hours=16)
        #         now1 = now+ timedelta(minutes=30)
        #         obj = Dist.objects.create(rp=rp_list[j], uid=i,exits=now1,enters=now)
        #         data['response']='sucess'
    return JsonResponse(data)

def stripper(t):
    t=t.replace(microsecond=0,hour=t.hour)
    t=datetime.strftime(t, "%H:%M")
    return t

def stripper1(t):
    min1=(int(t[3])*10+int(t[4]))/60.00
    min1=str(round(min1, 2)).strip('0')
    t=str(t[0])+str(t[1])+str(min1)
    
    return t

def classify(enters,exits):
    enters= stripper1(enters)
    exits= stripper1(exits)
    keys=list(dict1.keys())

    for i in range(len(keys)):
        keys1=keys[i].split('-')
        if float(enters)>float(keys1[0]):
            entrykey=keys1[0]

        if float(exits)<float(keys1[1]):
            exitkey=keys1[1]
            break

    list_keys=[]

    diff=int(exitkey)-int(entrykey)

    for i in range(1,diff+1):
        ran=str(int(entrykey)+1*(i-1))+'-'+str(int(entrykey)+1*i)
        list_keys.append(ran)
        dict1[ran]+=1
        
    return (str(list_keys))


@require_http_methods(['GET'])
@csrf_exempt
def viewv(request):
    if request.method == 'GET':
        for keys in dict1:
                dict1[keys]=0
        data={}
        temp = request.GET.get('rp')
        print(temp)
        if temp:
            query = Dist.objects.filter(rp=temp)

            list_entry = [obj.enters for obj in query]
            list_exit = [obj.exits for obj in query]

            for i in range(len(list_entry)):

                d = list_entry[i]
                dex = list_exit[i]

                enters = stripper(d)
                exits = stripper(dex)

                c=classify(enters,exits)

            total = query.count()
            data['total_visits']=total
            
            crowd_arr=""
            i=1
            for key in dict1:
                crowd_arr += str(dict1[key]+random.randint(0,8)) + ","
                i+=1
            crowd_arr = crowd_arr[0:len(crowd_arr)-1]
            data['crowd_freq']=crowd_arr
            # fig = plt.figure(figsize=(3,3))
            # plt.bar(list(dict1.keys()), dict1.values(), color='g')
            # plt.savefig(fig)
            

        return JsonResponse(data)

@require_http_methods(['GET'])
@csrf_exempt
def personal(request):
    if request.method == 'GET':
        data={}
        anal={}
        temp = request.GET.get('uid')
        if temp:
            query = Dist.objects.filter(uid=temp)
            list_rp= [obj.rp for obj in query]
            list_entry = [obj.enters for obj in query]
            list_exit = [obj.exits for obj in query]
            
            data['listrp']=str(list_rp)
            
            enterlist=[]
            exitlist=[]
            duration_list=[]

            for i in range(len(list_entry)):

                d = list_entry[i]
                dex = list_exit[i]

                enters = stripper(d)
                exits = stripper(dex)

                enterlist.append(enters)
                exitlist.append(exits)
            
            for i in range(len(list_entry)):
            
                FMT = '%H:%M'
                tdelta = (datetime.strptime(exitlist[i], FMT) - datetime.strptime(enterlist[i], FMT)).seconds/3600

                duration_list.append(tdelta)         
                anal[list_rp[i]]=(enterlist[i],exitlist[i],tdelta)
                print(anal[list_rp[i]])
                

            data['duration']=str(anal)

            labels = list_rp
            sizes = duration_list
            colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral','red','violet','grey','navy','yellow']
            patches, texts = plt.pie(sizes, colors=colors,labels=labels)
            # plt.axis('equal')
            # plt.tight_layout()
            # plt.show()


    return JsonResponse(data)


@require_http_methods(['POST'])
@csrf_exempt
def create_ref(req):
    if req.method == 'POST':
        body = req.body.json
        x = body['x']
        y = body['y']
        rname = body['rname']
        reg = body['reg']
        ReferencePoint.objects.create(name=rname,x=x,y=y,reg=reg)
        data = {
            'status': 'success'
        }
        return JsonResponse(data)

@require_http_methods(['GET'])
@csrf_exempt
def notify(request):
    if req.method == 'POST':
        body = req.body.json
        uid = body['uid']
        rp_now = body['rp_now']
        rp_details = ReferencePoint.objects.get(name = rp_now)
        all_rp = ReferencePoint.objects.all()
        rpx,rpy = rp_details.x, rp_details.y

        distance = 10000000000
        store = 0
        for i in range(len(all_rp)):
            temp = math.sqrt((rp_details[i].x - rpx)**2 + (rp_details[i].y - rpy)**2 )
            if dist < distance:
                distance = temp
                store = rp_details[i].name
        
        data = {
            'status': 'naren',
            'data':store
        }
        return JsonResponse(data)

@require_http_methods(['GET'])
@csrf_exempt    
def get_coord(req):
    if req.method=='GET':
        rname = req.GET.get('rname')
        results = ReferencePoint.objects.filter(name=rname)
        x_coord = results[0].x
        y_coord = results[0].y

        response={
            'status' : 'success',
            'data' : {
                'x' : x_coord,
                'y' : y_coord
            }
        }

        return JsonResponse(response)

@require_http_methods(['GET'])
@csrf_exempt
def draw_path(req):
    if req.method=='GET':
        img=cv2.imread("/home/ahmed/layout1.png")
        rp1=req.GET.get('rp1')
        rp2=req.GET.get('rp2')
        print(rp1,rp2)
        obj=ReferencePoint.objects.get(name=rp1)
        x1=obj.x
        y1=obj.y
        obj=ReferencePoint.objects.get(name=rp2)
        x2=obj.x
        y2=obj.y
        
        if(y2<y1 and x2 > x1):
            img=cv2.line(img,(x1,y1),(x1,y2),(255,0,0),3)
            img=cv2.line(img,(x1,y2),(x2,y2),(255,0,0),3)
        elif(y2>y1 and x2 < x1):
            print("hi")
            img=cv2.line(img,(x1,y1),(x2,y1),(255,0,0),3)
            img=cv2.line(img,(x2,y1),(x2,y2),(255,0,0),3)
        elif(y2<y1 and x2<x1):
            img=cv2.line(img,(x1,y1),(x1,y2),(255,0,0),3)
            img=cv2.line(img,(x1,y2),(x2,y2),(255,0,0),3)
        elif(y2>y1 and x2 > x1):
            img=cv2.line(img,(x1,y1),(x2,y1),(255,0,0),3)
            img=cv2.line(img,(x2,y1),(x2,y2),(255,0,0),3)
        img = cv2.circle(img,(x1,y1),5,(0,0,0),-1)
        img = cv2.circle(img,(x2,y2),5,(0,0,255),-1)
        cv2.imwrite("/home/ahmed/layout2.png",img)

        with open("/home/ahmed/layout2.png", "rb") as f:
            return HttpResponse(f.read(), content_type="image/bmp")

@require_http_methods(['GET'])
@csrf_exempt
def locate_me(req):
    if req.method=='GET':
        img=cv2.imread("/home/ahmed/layout1.png")
        rp1=req.GET.get('rp1')
        obj=ReferencePoint.objects.get(name=rp1)
        x1=obj.x
        y1=obj.y

        img = cv2.circle(img,(x1,y1),7,(50,255,255),-1)
        
        font = cv2.FONT_HERSHEY_SIMPLEX 
        
        # org 
        org = (50, 50) 
        
        # fontScale 
        fontScale = 0.5
        
        # Blue color in BGR 
        color = (255, 0, 0) 
        
        # Line thickness of 2 px 
        thickness = 1
        
        # Using cv2.putText() method 
        img = cv2.putText(img, 'You are here!',(x1+10,y1+2), font,  
                        fontScale, color, thickness, cv2.LINE_AA) 
        cv2.imwrite("/home/ahmed/layout3.png",img)

        with open("/home/ahmed/layout3.png", "rb") as f:
            return HttpResponse(f.read(), content_type="image/bmp")


@require_http_methods(['GET'])
@csrf_exempt
def get_offers(req):
    if req.method == 'GET':
        rp = req.GET.get('rp')
        obj=ReferencePoint.objects.get(name=rp)
        x1=obj.x
        y1=obj.y
        all_rp = ReferencePoint.objects.all()
        tmparr = []
        for rps in all_rp:
            if rps.reg == True:
                dis = math.sqrt((rps.x - x1)**2 + (rps.y-y1)**2)
                tmparr.append((dis,rps.name))
        
        tmparr.sort()

        offers_list1 = Offers.objects.filter(rp=tmparr[0][1])
        offers_list2 = Offers.objects.filter(rp=tmparr[1][1])
        tmp1 = []
        tmp=[]
        for f in offers_list1:
            tmp.append(f.desc)
        for f in offers_list2:
            tmp1.append(f.desc)

        results = {
                "rpname1" : tmparr[0][1],
                "offers1" : tmp[0],
                "rpname2" : tmparr[1][1],
                "offers2" : tmp1[0]
            }


        return JsonResponse(results)

@require_http_methods(['POST'])
@csrf_exempt
def get_wifi(req):
    if req.method=='POST':
        st= req.body
        #print(st)
        d = json.loads(st)
        tmp=json.loads(d['body'])
        a=[]
        our=['POCO PHONE', 'connect', 'Siemens', 'DIRECT-ZxDESKTOP-ICRIRH3ms2X', 'XL-Healthcare', 'moto']
        for t in tmp:
            if t['SSID'] in our:
                a.append((t['SSID'], t['level']))
        a= sorted(a, key = lambda x: x[1])
        print(a[-1])
        ref1=''
        if(a[-1][0] == 'POCO PHONE'):
            ref1='mentor_room'
        if(a[-1][0] == 'connect'):
            ref1='hack_room'
        if(a[-1][0] == 'Siemens'):
            ref1='stage'
        if(a[-1][0] == 'DIRECT-ZxDESKTOP-ICRIRH3ms2X'):
            ref1='game_room'
        if(a[-1][0] == 'XL-Healthcare'):
            ref1='regdesk'
        if(a[-1][0] == 'moto'):
            ref1='dining'
        
        #return JsonResponse(tmp, safe=False)
        
        img=cv2.imread("/home/ahmed/layout1.png")
        obj=ReferencePoint.objects.get(name=ref1)
        x1=obj.x
        y1=obj.y

        img = cv2.circle(img,(x1,y1),7,(50,255,255),-1)
        
        font = cv2.FONT_HERSHEY_SIMPLEX 
        
        # org 
        org = (50, 50) 
        
        # fontScale 
        fontScale = 0.5
        
        # Blue color in BGR 
        color = (255, 0, 0) 
        
        # Line thickness of 2 px 
        thickness = 1
        
        # Using cv2.putText() method 
        img = cv2.putText(img, 'You are here!',(x1+10,y1+2), font,  
                        fontScale, color, thickness, cv2.LINE_AA) 
        cv2.imwrite("/home/ahmed/layout3.png",img)

        result = {
            'name' : ref1
        }

        return JsonResponse(result)

@require_http_methods(['GET'])
@csrf_exempt
def get_image(req):
    if req.method=='GET':
        img=cv2.imread("/home/ahmed/layout3.png")
        with open("/home/ahmed/layout3.png", "rb") as f:
            return HttpResponse(f.read(), content_type="image/bmp")
