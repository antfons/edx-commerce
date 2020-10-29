from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Bid, Comment, Auction, Watchlist
from django import forms
from django.contrib.auth.decorators import login_required


class NewBidForm(forms.Form):
    bid = forms.FloatField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control col-lg-1'
            }
        )
    )


class NewListingForm(forms.Form):
    title = forms.CharField(
        label='Title',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Inform your title',
                'class': 'form-control col-lg-5'
            }
        )
    )
    description = forms.CharField(
        label='Description',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Write your description',
                'class': 'form-control col-lg-5'
            }
        )
    )
    photo_url = forms.CharField(
        label='Image url',
        required=False
    )
    category = forms.CharField(
        label='Category',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': '(Optional) Inform the category',
                'class': 'form-control col-lg-5'
            }
        )
    )
    initial_bid = forms.FloatField(
        required=True,
        min_value=0.1,
        label='Initial Bid',
        widget=forms.NumberInput(
            attrs={
                'step': '0.01',
                'class': 'form-control col-lg-1'
            }
        )
    )
    photo_url.widget.attrs.update({
        'placeholder': '(Optional) Inform the url of your image',
        'class': 'form-control col-lg-5'
        })


def get_watchlist_user(user_id):
    all_user_watchlist = Watchlist.objects.filter(user_id=user_id)
    return len(all_user_watchlist)


def index(request):
    listings = Auction.objects.all()
    watch_counter = 0
    if request.user.id:
        watch_counter = get_watchlist_user(request.user.id)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "watch_counter": watch_counter
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def add_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            photo_url = form.cleaned_data["photo_url"]
            category = form.cleaned_data["category"]
            initial_bid = form.cleaned_data["initial_bid"]
            user = User.objects.get(pk=request.user.id)
            auction = Auction(
                title=title,
                description=description,
                photo_url=photo_url,
                category=category,
                is_active=True,
                owner=user,
                initial_bid=initial_bid,
            )
            auction.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            watch_counter = 0
            if request.user.id:
                watch_counter = get_watchlist_user(request.user.id)
            return render(request, "auctions/add_listing.html", {
                "form": form,
                "watch_counter": watch_counter
    })
    watch_counter = 0
    if request.user.id:
        watch_counter = get_watchlist_user(request.user.id)
    return render(request, "auctions/add_listing.html", {
        "form": NewListingForm(),
        "watch_counter": watch_counter
    })


def listing(request, id):
    listing = Auction.objects.get(pk=id)
    watch_counter = 0
    if request.user.id:
        watch_counter = get_watchlist_user(request.user.id)
    higher_bid_obj = get_higher_bid_object(listing.bids.all())
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": NewBidForm(),
        "watch_counter": watch_counter,
        "comments": listing.comments.all(),
        "higher_bid": higher_bid_obj
    })

@login_required
def add_bid(request):
    if request.method == "POST":
        form = NewBidForm(request.POST)
        if form.is_valid():
            bid_value = form.cleaned_data["bid"]
            listing_id = request.POST.get('listing_id', '')
            listing = Auction.objects.get(pk=listing_id)
            bid_user = User.objects.get(pk=request.user.id)
            
            all_bids = listing.bids.all()
            if len(all_bids) != 0:
                higher_bid = max(bid.value for bid in all_bids)
                if bid_value > higher_bid:
                    new_bid = Bid(
                        value=bid_value,
                        user=bid_user
                    )
                    new_bid.save()
                    listing.bids.add(new_bid)
                    listing.save()

                    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
                else:
                    higher_bid_obj = get_higher_bid_object(listing.bids.all())
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "form": form,
                        "message": "Bid should be higher than current",
                        "higher_bid": higher_bid_obj
                    })
            else:
                if bid_value >= listing.initial_bid:
                    new_bid = Bid(
                        value=bid_value,
                        user=bid_user
                    )
                    new_bid.save()
                    listing.bids.add(new_bid)
                    listing.save()
                    return HttpResponseRedirect(
                        reverse("listing", args=(listing_id,)))
                else:
                    higher_bid_obj = get_higher_bid_object(listing.bids.all())
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "form": form,
                        "message": "Bid should be higher than current",
                        "comments": listing.comments.all(),
                        "higher_bid": higher_bid_obj
                    })

@login_required
def add_watchlist(request):
    if request.method == "POST":
        listing_id = request.POST.get('listing_id', '')
        watchlist_exist = Watchlist.objects.filter(
            auction_id=listing_id,
            user_id=request.user.id)
        if not watchlist_exist:
            user = User.objects.get(pk=request.user.id)
            auction = Auction.objects.get(pk=listing_id)
            watchlist = Watchlist(auction=auction, user=user)
            watchlist.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    
@login_required
def watchlist(request):
    if request.method == "GET":
        listings = []
        user_id = request.user.id
        watchlists = Watchlist.objects.filter(user_id=user_id)
        for watchlist in watchlists:
            listings.append(Auction.objects.get(pk=watchlist.auction_id))
    watch_counter = 0
    if request.user.id:
        watch_counter = get_watchlist_user(request.user.id)
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "watch_counter": watch_counter
    })

@login_required
def remove_watchlist(request):
    if request.method == "POST":
        listing_id = request.POST.get('listing_id', '')
        Watchlist.objects.filter(auction_id=listing_id, user_id=request.user.id).delete()
        return HttpResponseRedirect(reverse("watchlist"))


@login_required
def close_listing(request):
    if request.method == "POST":
        listing_id = request.POST.get('listing_id', '')
        listing = Auction.objects.get(pk=listing_id)
        listing.is_active = False
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required
def add_comment(request):
    if request.method == "POST":
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        listing_id = request.POST.get('listing_id', '')
        listing = Auction.objects.get(pk=listing_id)
        auction = Auction.objects.get(pk=listing_id)
        comment_text = request.POST.get('comment_text')
        comment = Comment(
            description=comment_text,
            commenter=user
        )
        comment.save()
        auction.comments.add(comment)
        auction.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def list_categories(request):
    if request.method == "GET":
        watch_counter = 0
        if request.user.id:
            watch_counter = get_watchlist_user(request.user.id)
        list_of_categories = []
        list_of_auctions = Auction.objects.all()
        for auction in list_of_auctions:
            list_of_categories.append(auction.category)
        list_of_categories = list(set(list_of_categories))
        return render(request, "auctions/categories.html", {
            "categories": list_of_categories,
            "watch_counter": watch_counter
        })


def list_by_category(request, category_name):
    listings = Auction.objects.filter(category=category_name)
    watch_counter = 0
    if request.user.id:
        watch_counter = get_watchlist_user(request.user.id)
    return render(request, "auctions/listing_by_category.html", {
        "listings": listings,
        "category": category_name,
        "watch_counter": watch_counter
    })


def get_higher_bid_object(list_of_bids):
    if len(list_of_bids) > 0:
        higher_bid = max(bid.value for bid in list_of_bids)
        bid_object = next(bid for bid in list_of_bids if bid.value == higher_bid)
        return bid_object
    return None
