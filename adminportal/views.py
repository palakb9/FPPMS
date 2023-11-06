from decimal import Context, ConversionSyntax
import json
import re
from django import contrib
from django.http.response import JsonResponse
from django.shortcuts import render
import rest_framework
from rest_framework import serializers
from rest_framework import response
from adminportal.serialization import AdminSerializationClass
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from FPPMS.models import Proposalmodel
from django.shortcuts import render
from rest_framework import status
import requests
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.models import User


@api_view(['GET']) 
def displayProposal(request):
    if request.method=='GET':
        results=Proposalmodel.objects.all()
        serialize=AdminSerializationClass(results,many=True)
        return Response(serialize.data)

def displayProposalList(request):
    results=Proposalmodel.objects.all()
    serialize=AdminSerializationClass(results,many=True)
    return render(request,'proposals.html',{'Proposalmodel': serialize.data})
    
#callapi = requests.get('https:///displayProposal')
#results = callapi.json()
#return render(request,'proposals.html',{'Proposalmodel': results})


# Create your views here.
def addAdmin(request):
    results = Proposalmodel.objects.all()
    return render(request, "addAdmin.html",{'Proposalmodel':results})

    
def dashboard(request):
    approved = 0;
    rejected = 0;
    split = 0;
    pending = 0;
    adminCount = User.objects.count()
    results = Proposalmodel.objects.all()

    for data in results:
        if(data.status == "Approved"):
            approved = approved + 1 ;
        if(data.status == "Rejected"):
            rejected = rejected + 1 ;
        if(data.status == "Split"):
            split = split + 1 ;
        if(data.status == "Pending"):
            pending = pending  + 1 ;

    final = {
        'Proposalmodel' : results,
        'approved' : approved,
        'rejected' : rejected,
        'split' : split,
        'pending' : pending,
        'adminCount' : adminCount,
    }
    return render(request, "dashboard.html", final)

def delete(request,pk):
    Proposalmodel.objects.filter(pk=pk).delete()
    results = Proposalmodel.objects.all()

    context = {
        'results' : results
    }
    return render(request, "proposals.html", {'Proposalmodel': results})

# def update(request,pk):
#     data = request.body
#     results = Proposalmodel.objects.filter(pk=pk)
#     serialize = AdminSerializationClass(results,data=data)
#     if serialize.is_valid():
#         serialize.save()
#         results = serialize.data
#         return render(request, "proposals.html", {'Proposalmodel': results})
#     return render(request, "proposals.html")

    
def update(request, pk):
    # TODO: clean data here
    payload = {}
    payload['fname'] = request.POST["fname"]
    payload['lname'] = request.POST["lname"]
    payload['phone'] = request.POST["phone"]
    payload['email'] = request.POST["email"]
    payload['userType'] = request.POST["userType"]
    payload['ptitle'] = request.POST["ptitle"]
    payload['pdesc'] = request.POST["pdesc"]
    payload['status'] = request.POST["status"]
    payload['pwebsite'] = request.POST["pwebsite"]
    payload['comment'] = request.POST["comment"]
    payload['reference'] = request.POST["reference"]
    payload['document'] = request.POST["document"]

    # save
    proposal = Proposalmodel.objects.get(id=pk)
    serializer = AdminSerializationClass(proposal, data=payload, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return redirect('proposals')

    # in case you want to return the json of the data
    # result = serializer.data
    # return JsonResponse(result)

       
# def proposalCount(request):
#     proposals = Proposalmodel.objects.all()
#     totalProposal_count = proposals.count()

#     context = {
#         'proposals' : proposals,
#         'totalProposal_count' : totalProposal_count
#     }

#     return render(request, 'dashboard.html' , context)

def send_dictionary(request):
    proposals = Proposalmodel.objects.all()
    totalProposal_count = proposals.count()
    dataDictionary = {
        'totalProposal' : totalProposal_count,
    }

    dataJSON = json.dumps(dataDictionary)
    return render(request, 'proposals.html', {'data': dataJSON})