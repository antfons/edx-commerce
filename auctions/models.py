from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    def __str__(self):
        return f"Id: {self.id} Name: {self.username}"


class Bid(models.Model):
    value = models.FloatField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_bid")

    def __str__(self):
        return f"Value: {self.value}. User: {self.user}"


class Comment(models.Model):
    description = models.CharField(max_length=250)
    commenter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user")

    def __str__(self):
        return f"Id: {self.id} Description: {self.description} Commenter: {self.commenter}"


class Auction(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    photo_url = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(
        default=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owner_user")
    initial_bid = models.FloatField()
    bids = models.ManyToManyField(Bid, blank=True, related_name="bids")
    comments = models.ManyToManyField(Comment, blank=True, related_name="auctions")
    creation_date = models.DateTimeField(
        default=now
    )

    def __str__(self):
        return f"Id: {self.id} Title: {self.title} Description: {self.description}. Category: {self.category} Init_Bid: {self.initial_bid} Current_Bid: { max(bid.value for bid in self.bids.all()) if len(self.bids.all()) > 0 else None}"


class Watchlist(models.Model):
    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Id: {self.id}. Auction: {self.auction}. User: {self.user}"
