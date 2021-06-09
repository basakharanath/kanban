from rest_framework import serializers
from .models import *


class cardAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardAttachment
        fields = '__all__'


class cardSerializer(serializers.ModelSerializer):
    attachment_details = cardAttachmentSerializer(many=True)
    class Meta:
        model = Card
        fields = '__all__'

class listSerializer(serializers.ModelSerializer):
    card_details = cardSerializer(many=True)
    class Meta:
        model = List
        fields = '__all__'

class boardSerializer(serializers.ModelSerializer):
    list_details = listSerializer(many=True)
    class Meta:
        model = Board
        fields = '__all__'

class userSerializer(serializers.ModelSerializer):
    board_details = boardSerializer(many=True)
    class Meta:
        model = User
        fields = '__all__'