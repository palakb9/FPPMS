import re
from FPPMS.models import Proposalmodel
from FPPMS.serialize import Proposalserialize
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import requests
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.db import connection
from FPPMS.settings import EMAIL_HOST_USER

@api_view(['POST'])
def saveproposal(request):
    if request.method=="POST":
        saveserialize=Proposalserialize(data=request.data)
        if saveserialize.is_valid():
            saveserialize.save()
            return Response(saveserialize.data,status=status.HTTP_201_CREATED)
        return Response(saveserialize.errors,status=status.HTTP_400_BAD_REQUEST)


def insertproposal(request):
    if request.method=="POST":
        title=request.POST.get('title')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        userType=request.POST.get('userType')
        status=request.POST.get('status')
        ptitle=request.POST.get('ptitle')
        pwebsite=request.POST.get('pwebsite')
        pdesc=request.POST.get('pdesc')
        comment=request.POST.get('comment')
        reference=request.POST.get('reference')
        document=request.POST.get('document')

        data={'title':title,'fname':fname,'lname':lname,'phone':phone,'email':email,'userType':userType,'status':status,'ptitle':ptitle,'pdesc':pdesc,'pwebsite':pwebsite,'comment':comment,'reference':reference,'document':document}
        headers={'Content-Type': 'application/json'}
        saveserialize=Proposalserialize(data=data)
        if saveserialize.is_valid():
            
            read = saveserialize.save()
        
        #read=requests.post('http://184.107.41.83/Insertproposal',json=data,headers=headers)
            if(read):
                messages.success(request,'Your proposal was successfully registered!')
                emails = prepareEmailForSenders()
                sub , msg = getEmailBody()
                for email in emails:
                    send_mail(sub,msg,EMAIL_HOST_USER,[email],fail_silently=False)
                return render(request,'index.html')
            else:
                messages.success(request,'INVALID!')
                return render(request,'index.html')
        
    else:
        return render(request,'index.html')

def getProjectDetails():
    with connection.cursor() as cursor:
        cursor.execute("SELECT title, concat(fname ,' ', lname) FROM `proposals` as p order by p.id desc")
        row = cursor.fetchone()
    return row

def getEmailBody():
    row = getProjectDetails()
    msg = 'Dear Admin,\r\n\nA new proposal has been submitted in the system by '+row[1] + '.\r\n\nRegards,\r\nFPPMS Team'
    title  = 'New Proposal Received : ' +row[0]
    return title, msg

def my_custom_sql():
    with connection.cursor() as cursor:
        cursor.execute("SELECT email FROM `auth_user` where is_superuser = 1")
        rows = cursor.fetchall()
    return rows    

def prepareEmailForSenders():
    rows = my_custom_sql()
    emails = list()
    for sig in rows:
        emails.append(sig[0])
    return emails


def aboutus(request):
    return render(request, "GetToKnowUs.html")

def faq(request):
    return render(request, "FAQ.html")


