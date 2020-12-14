from django.db import models

class Park(models.Model):
    pid=models.CharField(max_length=100,default="P")
    uid = models.IntegerField(default=0)
    pos_x = models.IntegerField()
    pos_y = models.IntegerField()
    status = models.CharField(max_length=30)