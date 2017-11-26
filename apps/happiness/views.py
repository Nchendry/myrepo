from __future__ import unicode_literals
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse
from models import * 

def index(request):
    return render(request, 'happiness/index.html')

def register(request):
    result = User.objects.validate(request.POST)
    if result[0]:
        request.session['user'] = result[1].id
        request.session['name'] = result[1].name
        request.session['username'] = result[1].username
        return redirect('/travels')
    else:
        for error in result[1]:
            messages.add_message(request,messages.INFO, error)
        return redirect('/main')

def login(request):
    result = User.objects.login(request.POST)
    if result[0]:
        request.session['user'] = result[1].id
        request.session['name'] = result[1].name
        request.session['username'] = result[1].username
        return redirect('/travels')
    else:
        for error in result[1]:
            messages.add_message(request,messages.INFO, error)
            return redirect('/main')

def travels(request):
    user = User.objects.get(id = request.session['user'])
    # print user.joinedby.destination
    # {% endfor %}</h2>
    # {% for test in test1 %}
    # {{test.plannedby.id}}
    # {% endfor %}
    context = {
        'users': User.objects.get(id = request.session['user']),
        'trips': user.joinedby.all(),
        'mytrips': Trip.objects.filter(plannedby_id = request.session['user']),
        'othertrips': Trip.objects.exclude(plannedby_id=request.session['user'])
    }
    
    return render(request, 'happiness/travels.html', context)

def add(request):
    context = {
        'users': User.objects.get(id = request.session['user'])
    }
    return render(request, 'happiness/add.html', context)

def addtravels(request):
    Trip.objects.create (
        destination = request.POST['dest'],
        description = request.POST['desc'],
        plannedby = User.objects.get(id = request.POST['user_id']),
        fromdate = request.POST['fromdate'],
        todate = request.POST['todate'],
    )
    return redirect('/travels')

def logout(request):
    request.session.clear()
    return redirect('/')

def home(request):
    return redirect('/travels')

def destination(request, id):
    trip = Trip.objects.get(id = id).joining.all()
    context = {
        'trips': Trip.objects.get(id = id),
        'joining': trip
    }
    return render(request, 'happiness/destination.html', context)

def join(request, id):
    
    trip = Trip.objects.get(id = id)
    user = User.objects.get(id = request.session['user'])
    user.joinedby.add(trip)
    return redirect('/travels')