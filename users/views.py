from django.shortcuts import render
import os
import logging
from rest_framework.views import APIView
from rest_framework import viewsets, request
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.conf import settings
from django.db.models import Q
from django.db import connection
import hashlib
from hashlib import md5
import re
from .models import *


Logger = logging.getLogger(__name__)
# Create your views here.

@api_view(['POST'])
def user_login(request):
    """
        User Login
        
        Requests:
            username : Email Id or Phone No.
            password : 
        
        Response:
            Message
            Response Data
            Error
    """
    result =  None
    message = None
    error = None
    try:
        data = request.data
        cursor = connection.cursor()
        Logger.info(f"Request Data : {data}")
        username = data['username']
        password = data['password']
        password = str(password).encode('utf-8')
        password = hashlib.md5(password)
        password = password.hexdigest()
        q1 = User.objects.filter(Q(email_id=username) | Q(phone_no=username))
        if q1:
            Logger.info("Valid Username")
            query = f"""SELECT user_id, user_type, concat(user_firstname,' ',user_lastname) as user_name, email_id, phone_no, password
	                    FROM "user" WHERE email_id = '{username}' or phone_no = '{username}'; """
            cursor.execute(query)
            # row = cursor.fetchall()
            # Logger.info(f"Row Result : {row}")
            cols = [col[0] for col in cursor.description]
            user_details = [
                    dict(zip(cols,rows))
                    for rows in cursor.fetchall()
                ][0]
            Logger.info(f"User Details : {user_details}")
            if user_details['password'] == password:
                user_details.pop("password")
                result = user_details
                message = "Login Successful"
            else:
                message = "Invalid Password"
        else:
            Logger.info("Invalid Username")
            message = "Invalid Username"
    except Exception as e:
        Logger.info(f"Exception : {e}")
        error = "System Error"
    return Response({"Message" : message, "Response Data" : result, "Error" : error})


@api_view(['POST'])
def user_signup(request):
    """
        User Sign Up
        
        Requests:
            password
            user_firstname
            user_lastname
            email_id
            phone_no
            user_type
        
        Response:
            Message
            Response Data
            Error
    """
    result =  None
    message = None
    error = None
    try:
        data = request.data
        Logger.info(f"Request Data : {data}")
        user_email = data['email_id']
        user_phone = data['phone_no']
        password = data['password']
        q1 = User.objects.filter(Q(email_id=user_email) | Q(phone_no=user_phone))
        if q1:
            Logger.info("You are a existing user")
            message = "You are a existing user"
        else:
            Logger.info(f"New User")
            if re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$",user_email) and re.match(r"^[6789]{1}\d{9}$", user_phone):
                password = str(password).encode('utf-8')
                password = hashlib.md5(password)
                password = password.hexdigest()
                Logger.info('Password converted to Encoded string')
                data['password'] = password
                user_instance = User.objects.create(**data)
                message = "Sign Up Successfully Done"
            else:
                Logger.info("Invalid Email Id or Phone No Format")
                message = "Invalid Email Id or Phone No Formate"
    except Exception as e:
        Logger.info(f"Exception : {e}")
        error = "System Error"
    return Response({"Message" : message, "Response Data" : result, "Error" : error})
