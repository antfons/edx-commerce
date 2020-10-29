from django.contrib import admin

from .models import *
# Register your models here.

class AuctionAdmin(admin.ModelAdmin):
    filter_horizontal = ("comments", "bids")


admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Auction, AuctionAdmin)