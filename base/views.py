import datetime
from typing import Any
from django.core.files.base import ContentFile
from django.forms.widgets import HiddenInput
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Attendants, Feedbacks, Offers, Tags, Profiles
from .forms import ApproveForm, FeedbackForm, OffersForm, StatusForm, AttendeeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
#from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.db import models
from django.db.models import Q

from base import forms

# Create your views here.

def loginUser(request):
    page='login'

    if request.user.is_authenticated:
        return redirect ('events')

    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not registered")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('events')
        else:
            messages.error(request,'username or password is incorrect')

    return render(request, 'login_register.html')

def logoutUser(request):
    logout(request)
    messages.error(request, "User is succesfuly logged out")
    return redirect('login_register')

def signin(request):
    return render(request, 'signin.html')

def activity(request):
    return render(request, 'activity.html')

@login_required(login_url='login_register')
def profile(request, pk):
    profile = Profiles.objects.get(username=pk)
    offerList =Offers.objects.filter(owner=profile)
    context = {'profile':profile, 'offerList':offerList}
    return render(request, 'profile.html', context)

@login_required(login_url='login_register')
def account(request):
    account = request.user.profiles
    offerList =Offers.objects.filter(owner=account)
    context = {'account':account, 'offerList': offerList}
    return render(request, 'account.html', context)

@login_required(login_url='login_register')
def profiles(request):
    profiles = Profiles.objects.all()
    context = {'profiles':profiles}
    return render(request, 'profiles.html', context)

def register(request):
    page='register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account is created!')
            login(request, user)
            return redirect('events')
            
        else:
            messages.success(request, 'An error has occurred during the registration!')

    context = {'page':page, 'form':form}
    return render(request, 'login_register.html', context)

def signin(request):
    return render(request, 'createevent.html')

@login_required(login_url='login_register')
def events(request):

    search_query='aaa'
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    eventsObj = Offers.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query) | Q(location__icontains=search_query))
    profile = request.user.profiles
    context = {'Events': eventsObj, 'profile': profile, 'search_query':search_query}
    return render(request, 'events.html', context)

@login_required(login_url='login_register')
def event(request, pk):
    eventObj = Offers.objects.get(offerid=pk)
    hashtags = eventObj.hashtags.all()
    context = {'hashtags': hashtags}
    profile = request.user.profiles
    attendanceObj = Attendants.objects.filter(event=pk)
    feedbackObj = Feedbacks.objects.filter(offer=pk)
    print(attendanceObj.filter(status='approved').count())

    form = ApproveForm(initial={'status': 'approval'})
    form.status = 'approval'
    
    if request.method == 'POST':
        if profile != eventObj.owner:
            form = ApproveForm(request.POST)
            approval = form.save(commit=False)
            approval.owner = profile
            approval.event = eventObj
            approval.status = 'approval'
            
            if profile.credits < eventObj.credits:
                messages.success(request, 'Your credit is not sufficient!')
                approval.status = 'rejected'
            else:
                approval.save()
                messages.success(request, 'Your attendance request is completed!')

        else:
            for i in attendanceObj:
                form = ApproveForm(request.POST, instance=i)
                approval = form.save(commit=False)
                approval.owner = i.owner
                approval.event = i.event
                profile = Profiles.objects.get(username=i.owner)
                print(approval.status.count('approved'))
                
                if (approval.status == 'approved') and (attendanceObj.filter(status='approved').count()) < (eventObj.numberOfParticipants):
                    messages.success(request, 'Your approval selection is completed!')
                    approval.save()
                elif(approval.status == 'approved') and (attendanceObj.filter(status='approved').count()) >= (eventObj.numberOfParticipants):
                    messages.success(request, 'You reached the maximum number of attendees!')
                    approval.status='rejected'
                    approval.save()   
                    
    
                break   
        
    return render(request, 'event.html', {'eventObj': eventObj, 'hashtags':hashtags, 'form':form, 'profile':profile,'attendanceObj':attendanceObj, 'feedbackObj':feedbackObj})

@login_required(login_url='login_register')
def createevent(request):
    profile = request.user.profiles
    form = OffersForm()

    if request.method == 'POST':
        form = OffersForm(request.POST, request.FILES)
        if form.is_valid():
            if len(request.FILES) != 0:
                form.picture = request.FILES['picture']

            event = form.save(commit=False)
            event.owner = profile
            event.eventstatus = 'inprogress'
            if event.type == "gathering" and event.credits != 0:
                messages.success(request, 'For gatherings, number of credits should be zero!')
                event.credits = 0
            
            
            event.save()
            return redirect('events')

    context={'form': form, 'profile':profile}
    return render(request, 'createevent.html', context)

@login_required(login_url='login_register')
def updateevent(request, pk):
    profile = request.user.profiles
    event = profile.offers_set.get(offerid = pk)
    form = OffersForm(instance = event)

    if request.method == 'POST':
        form = OffersForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            if len(request.FILES) != 0:
                form.picture = request.FILES['picture']

            if event.type == "gathering" and event.credits != 0:
                messages.success(request, 'For gatherings, number of credits should be zero!')
                event.credits = 0

            form.save()
            return redirect('events')

    context={'form': form}
    return render(request, 'createevent.html', context)

@login_required(login_url='login_register')
def deleteevent(request, pk):
    profile = request.user.profiles
    eventObj = Offers.objects.get(offerid = pk)
    attendanceObj = Attendants.objects.filter(event=pk)
    form = StatusForm(instance = eventObj)
    if request.method =='POST':
            form = StatusForm(request.POST, instance = eventObj)
            status = form.save(commit=False)
            status.save()
            if eventObj.owner != profile:
                messages.warning(request, 'You are not allowed to update this page')
                return redirect('')
            elif (eventObj.owner == profile) and (status.eventstatus == 'done') and (datetime.date.today()>eventObj.date):
                status.eventstatus = 'done'
                status.save()
            '''''
                for i in attendanceObj:
                    #form = StatusForm(request.POST)
                    if i.status=='approved':
                        profile = Profiles.objects.get(username=i.owner)
                        profile.credits = (profile.credits - eventObj.credits)
                        profile.save()
                
                profile = request.user.profiles
                profile.credits = (profile.credits + eventObj.credits)
                profile.save()
            elif (eventObj.owner == profile) and (status.eventstatus == 'canceled'):
                    status.save()
                    eventObj.save()
            '''''
            return redirect('events')
    return render(request, 'deleteevent.html', {'eventObj':eventObj, 'form':form, 'profile':profile, 'attendanceObj':attendanceObj})

@login_required(login_url='login_register')
def feedback(request, pk):
    feedbackObj = Feedbacks.objects.filter(offer=pk)
    eventObj = Offers.objects.get(offerid = pk) 
    form = FeedbackForm()
    profile = request.user.profiles
    

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        status = form.save(commit=False)
        status.owner = profile
        status.offer = eventObj
        status.save()

        return redirect('events')

    context = {'feedbackObj':feedbackObj, 'form':form, 'eventObj':eventObj, 'profile':profile}
    return render(request, 'feedback.html', context)

def approve(request, pk, sk):
    eventObj = Offers.objects.get(offerid=pk)
    profile = request.user.profiles
    attendanceObj = Attendants.objects.filter(event=pk, owner=sk)
    attendanceNum = Attendants.objects.filter(event=pk)
    print(attendanceObj.filter(status='approved').count())
    form = ApproveForm()
    if request.method == 'POST':
        for i in attendanceObj:
            if profile == eventObj.owner:
                form = ApproveForm(request.POST, instance=i)
                approval = form.save(commit=False)
                approval.owner = i.owner
                approval.event = i.event
                    
                if (approval.status == 'approved') and (attendanceNum.filter(status='approved').count()) < (eventObj.numberOfParticipants):
                    messages.success(request, 'Your approval selection is completed!')
                    approval.save()
                elif(approval.status == 'approved') and (attendanceNum.filter(status='approved').count()) >= (eventObj.numberOfParticipants):
                    messages.success(request, 'You reached the maximum number of attendees!')
                    approval.status='rejected'
                    approval.save()

    context = {'eventObj':eventObj, 'profile':profile, 'form':form, 'attendanceObj':attendanceObj}
    return render(request, 'approve.html', context)


def creditexchange(request, pk, sk):
    eventObj = Offers.objects.get(offerid=pk)
    profile = request.user.profiles
    attendanceObj = Attendants.objects.filter(event=pk, owner=sk)
    form = AttendeeForm()
    if request.method == 'POST':
        for i in attendanceObj:
            form = AttendeeForm(request.POST, instance = i)
            status = form.save(commit=False)
            status.save()
            if (i.offerstatus == 'done') and (eventObj.eventstatus=='done') and (datetime.date.today()>eventObj.date) and (i.exchange=='no'):
                profile.credits = profile.credits - eventObj.credits
                i.exchange = 'yes'
                i.save()
                profile.save()
                status.save()
                if eventObj.exchange == 'no':
                    eventObj.owner.credits = eventObj.owner.credits + eventObj.credits
                    eventObj.exchange = 'yes'
                    eventObj.save()
                    eventObj.owner.save()
                    status.save()
    
    context = {'eventObj':eventObj, 'profile':profile, 'form':form, 'attendanceObj':attendanceObj}
    return render(request, 'creditexchange.html', context)
    

def gatherings(request):
    return render(request, 'gatherings.html')

def creategathering(request):
    return render(request, 'creategathering.html')
