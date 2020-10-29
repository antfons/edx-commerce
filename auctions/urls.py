from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("listings/<str:id>", views.listing, name="listing"),
    path("add_bid", views.add_bid, name="add_bid"),
    path("add_to_watchlist", views.add_watchlist, name="add_to_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("remove_watchlist", views.remove_watchlist, name="remove_watchlist"),
    path("close_listing", views.close_listing, name="close_listing"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("list_categories", views.list_categories, name="list_categories"),
    path("list_by_category/<str:category_name>", views.list_by_category, name="list_by_category")
]
