from django.db import models
from django.contrib.auth.models import User


class Venue(models.Model):
    name = models.CharField(max_length=80)
    def __str__(self):
        return self.name


class Concert(models.Model):
    name = models.CharField(max_length=100)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    image = models.CharField(max_length=256)
    def __str__(self):
        return self.name


class ConcertSeat(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name='seats')
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(null=False)
    occupancy = models.PositiveBigIntegerField(null=False)
    price = models.FloatField(null=False)
    def __str__(self):
        return f"{self.concert.name} - {self.name}"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_cost = models.FloatField()
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)


class TransactionTicket(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    seat = models.ForeignKey(ConcertSeat, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.count}"


class ExtendUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=500)
    def __str__(self):
        return str(self.user)