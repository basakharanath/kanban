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

