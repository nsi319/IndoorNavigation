from django.db import models

class Dist(models.Model):
    rp = models.CharField(max_length=100)
    uid = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    enters = models.DateTimeField()
    exits = models.DateTimeField()


class ReferencePoint(models.Model):
    name = models.CharField(max_length=100)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    reg = models.BooleanField(default=False)

    def __str__(self):
        return  self.name

class Offers(models.Model):
    rp = models.CharField(max_length=100)
    desc = models.CharField(max_length=300)

    