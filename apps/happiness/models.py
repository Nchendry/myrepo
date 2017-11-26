# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import bcrypt
import re
import datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from django.db import models

class UserManager(models.Manager):
    
    def login(self, POST):
        errors = []
        if len(POST['username']) == 0:
            errors.append('Please enter a valid username')
        if len(POST['password']) == 0:
            errors.append('Please enter a valid password')
        if len(User.objects.filter(username = POST['username'])) < 1 or not bcrypt.checkpw(POST['password'].encode(), User.objects.get(username = POST['username']).password.encode()):
            errors.append('wrong username and password combo')
        if len(errors) > 0:
            return (False, errors) # return the list of errors
        else:
            user = User.objects.get(username = POST['username'])
            return (True, user)

    def validate(self, POST):
        errors = []
        if len(POST['name']) == 0:
            errors.append('First Name is required')
        if len(POST['username']) == 0:
            errors.append('username is required')
        if len(User.objects.filter(username = POST['username'])) > 0:
            errors.append('username already in use')
        if len(POST['password']) == 0:
            errors.append('Password is required')
        if POST['password'] != POST['confirm_password']:
            errors.append('Passwords do not match')
        # user_check = User.objects.get(email = POST['email'])
        if len(User.objects.filter(username = POST['username'])) > 0:
            errors.append('duplicate username')
        # if len(user_check) == 0:
        if len(errors) > 0:
            return (False, errors) # return the list of errors
        else:
            # save the information
            new_user = User.objects.create(
                name = POST['name'],
                username = POST['username'],
                password = bcrypt.hashpw(POST['password'].encode(), bcrypt.gensalt()),
            )
            # then what?
            return (True, new_user)

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    plannedby = models.ForeignKey(User, related_name='trips')
    joining = models.ManyToManyField(User, related_name='joinedby')
    fromdate = models.DateField(datetime.date)
    todate = models.DateField(datetime.date)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


# Create your models here.
