from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    user_type = models.IntegerField()
    user_firstname = models.CharField(max_length=100)
    user_lastname = models.CharField(max_length=100)
    email_id = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=20)
    password = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'user'


class Board(models.Model):
    board_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, related_name='board_details')
    boards_name = models.CharField(max_length=100)
    boards_description = models.CharField(max_length=250, blank=True, null=True)
    board_created_on = models.DateTimeField(auto_now_add = True)
    board_updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'board'


class List(models.Model):
    list_id = models.AutoField(primary_key=True)
    board = models.ForeignKey(Board, models.DO_NOTHING, related_name='list_details')
    list_name = models.CharField(max_length=100)
    list_description = models.CharField(max_length=250, blank=True, null=True)
    list_created_on = models.DateTimeField(auto_now_add = True)
    list_updated_on = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'list'


class Card(models.Model):
    card_id = models.AutoField(primary_key=True)
    list = models.ForeignKey('List', models.DO_NOTHING, related_name='card_details')
    card_name = models.CharField(max_length=100)
    card_description = models.CharField(max_length=250, blank=True, null=True)
    card_created_on = models.DateTimeField(auto_now_add = True)
    card_updated_on = models.DateTimeField(blank=True, null=True)
    card_due_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'card'


class CardAttachment(models.Model):
    card_attachment_id = models.AutoField(primary_key=True)
    card = models.ForeignKey(Card, models.DO_NOTHING,  related_name = 'attachment_details')
    attachment_ref = models.TextField()
    attachment_date = models.DateTimeField(auto_now_add = True)

    class Meta:
        managed = False
        db_table = 'card_attachment'
