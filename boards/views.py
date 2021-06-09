from django.shortcuts import render
import os
import logging
from rest_framework.views import APIView
from rest_framework import viewsets, request
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.conf import settings
from django.db import connection
from datetime import datetime
from .models import *
from .serializers import *


Logger = logging.getLogger(__name__)

# Create your views here.

@api_view(['POST'])
def board_details(request):
    """
        Board Details By User 
        
        Requests:
            user_id
        Response:
            Message
            Response Data
            Error
    """
    result =  None
    message = None
    error = None
    try:
        cursor = connection.cursor()
        data = request.data
        Logger.info(f"Request Data : {data}")
        user_id = data['user_id']

        q1 = User.objects.filter(user_id = user_id)
        if q1:
            Logger.info('User Exists in database')
            serializer = userSerializer(q1,many=True)
            details = serializer.data
            details[0].pop('password')
            result = details[0]
    except Exception as e:
        Logger.info(f"Exception : {e}")
        error = "System Error"
    return Response({"Message" : message, "Response Data" : result, "Error" : error})

#! Create Board
@api_view(['POST'])
def create_board(request):
    """
        Create Board 
        
        Requests:
            user_id
            boards_name
            boards_description
        Response:
            Message
            Response Data
            Error
    """
    result =  None
    message = None
    error = None
    try:
        cursor = connection.cursor()
        data = request.data
        Logger.info(f"Request Data : {data}")
        user_id = data['user_id']
        query = f"""SELECT user_type FROM "user" WHERE user_id = {user_id};"""
        cursor.execute(query)
        row = cursor.fetchall()
        user_type = row[0][0]
        Logger.info(f"User Type : {user_type}")
        if user_type == 2:
            Logger.info("Premium User")
            Board.objects.create(**data)
            message = "Board successfully created"
        else:
            Logger.info("Free User")
            board_count = Board.objects.filter(user=user_id).count()
            Logger.info(f"Board Count : {board_count}")
            if board_count < 10:
                Board.objects.create(**data)
                message = "Board successfully created"
            else:
                message = "Please upgrade your account to add more board"
    except Exception as e:
        Logger.info(f"Exception : {e}")
        error = "System Error"
    return Response({"Message" : message, "Response Data" : result, "Error" : error})


#! Update Board
@api_view(['POST'])
def update_board(request):
    """
        Create Board 
        
        Requests:
            board_id
            boards_name
            boards_description
        Response:
            Message
            Response Data
            Error
    """
    result =  None
    message = None
    error = None
    try:
        cursor = connection.cursor()
        data = request.data
        Logger.info(f"Request Data : {data}")
        board_id = data['board_id']
        if Board.objects.filter(board_id=board_id).exists():
            current_date = datetime.now()
            data['board_updated_on'] = current_date
            Board.objects.filter(board_id=board_id).update(**data)
            message = "Board successfully updated"
        else:
            message = "Board does not exist"
    except Exception as e:
        Logger.info(f"Exception : {e}")
        error = "System Error"
    return Response({"Message" : message, "Response Data" : result, "Error" : error})


#! Create List
@api_view(['POST'])
def create_list(request):
    """
        Create List 
        
        Requests:
            board_id
            list_name
            list_description
        Response:
            Message
            Response Data
            Error
    """
    result =  None
    message = None
    error = None
    try:
        cursor = connection.cursor()
        data = request.data
        Logger.info(f"Request Data : {data}")
        board_id = data['board_id']
        if Board.objects.filter(board_id=board_id).exists():
            List.objects.create(**data)
            message = "List successfully created"
        else:
             message = "Board does not exist"
    except Exception as e:
        Logger.info(f"Exception : {e}")
        error = "System Error"
    return Response({"Message" : message, "Response Data" : result, "Error" : error})



#! Update List
@api_view(['POST'])
def update_list(request):
    """
        Update List 
        
        Requests:
            list_id
            list_name
            list_description
        Response:
            Message
            Response Data
            Error
    """
    result =  None
    message = None
    error = None
    try:
        cursor = connection.cursor()
        data = request.data
        Logger.info(f"Request Data : {data}")
        list_id = data['list_id']
        if List.objects.filter(list_id=list_id).exists():
            current_date = datetime.now()
            data['list_updated_on'] = current_date
            List.objects.filter(list_id=list_id).update(**data)
            message = "List successfully updated"
        else:
             message = "List does not exist"
    except Exception as e:
        Logger.info(f"Exception : {e}")
        error = "System Error"
    return Response({"Message" : message, "Response Data" : result, "Error" : error})




#! Create Card
@api_view(['POST'])
def create_card(request):
    """
        Create Card
        
        Requests:
            list_id
            card_name
            card_description
            card_due_date
        Response:
            Message
            Response Data
            Error
    """
    result =  None
    message = None
    error = None
    try:
        cursor = connection.cursor()
        data = request.data
        Logger.info(f"Request Data : {data}")
        list_id = data['list_id']
        if List.objects.filter(list_id=list_id).exists():
            Card.objects.create(**data)
            message = "Card successfully created"
        else:
             message = "List does not exist"
    except Exception as e:
        Logger.info(f"Exception : {e}")
        error = "System Error"
    return Response({"Message" : message, "Response Data" : result, "Error" : error})



#! Update Card
@api_view(['POST'])
def update_card(request):
    """
        Update Card
        
        Requests:
            card_id
            card_name
            card_description
            card_due_date
        Response:
            Message
            Response Data
            Error
    """
    result =  None
    message = None
    error = None
    try:
        cursor = connection.cursor()
        data = request.data
        Logger.info(f"Request Data : {data}")
        card_id = data['card_id']
        if Card.objects.filter(card_id=card_id).exists():
            current_date = datetime.now()
            data['card_updated_on'] = current_date
            Card.objects.filter(card_id=card_id).update(**data)
            message = "Card successfully updated"
        else:
             message = "Card does not exist"
    except Exception as e:
        Logger.info(f"Exception : {e}")
        error = "System Error"
    return Response({"Message" : message, "Response Data" : result, "Error" : error})



#! Move Card to another list
@api_view(['POST'])
def move_card(request):
    """
        Move Card
        
        Requests:
            card_id
            list_id
        Response:
            Message
            Response Data
            Error
    """
    result =  None
    message = None
    error = None
    try:
        cursor = connection.cursor()
        data = request.data
        Logger.info(f"Request Data : {data}")
        card_id = data['card_id']
        list_id = data['list_id']
        if List.objects.filter(list_id=list_id).exists():
            if Card.objects.filter(card_id=card_id).exists():
                card_updated_on = datetime.now()
                Card.objects.filter(card_id=card_id).update(list = list_id,card_updated_on = card_updated_on)
                message = "Card successfully moved"
            else:
                message = "Card does not exist"
        else:
             message = "List does not exist"
    except Exception as e:
        Logger.info(f"Exception : {e}")
        error = "System Error"
    return Response({"Message" : message, "Response Data" : result, "Error" : error})

#! Create Card Attachment
@api_view(['POST'])
def create_card_attachment(request):
    """
        Create Card Attachment
        
        Requests:
            card_id
            attachment_ref
        Response:
            Message
            Response Data
            Error
    """
    result =  None
    message = None
    error = None
    try:
        cursor = connection.cursor()
        data = request.data
        Logger.info(f"Request Data : {data}")
        card_id = data['card_id']
        if Card.objects.filter(card_id=card_id).exists():
            CardAttachment.objects.create(**data)
            message = "Card attachment successfully"
        else:
             message = "Card does not exist"
    except Exception as e:
        Logger.info(f"Exception : {e}")
        error = "System Error"
    return Response({"Message" : message, "Response Data" : result, "Error" : error})



#! Update Card Attachment
@api_view(['POST'])
def update_card_attachment(request):
    """
        Update Card Attachment
        
        Requests:
            card_attachment_id
            attachment_ref
        Response:
            Message
            Response Data
            Error
    """
    result =  None
    message = None
    error = None
    try:
        cursor = connection.cursor()
        data = request.data
        Logger.info(f"Request Data : {data}")
        card_attachment_id = data['card_attachment_id']
        if CardAttachment.objects.filter(card_attachment_id=card_attachment_id).exists():
            current_date = datetime.now()
            data['card_updated_on'] = current_date
            CardAttachment.objects.filter(card_attachment_id=card_attachment_id).update(**data)
            message = "Card attachment successfully updated"
        else:
             message = "Card attachment does not exist"
    except Exception as e:
        Logger.info(f"Exception : {e}")
        error = "System Error"
    return Response({"Message" : message, "Response Data" : result, "Error" : error})
