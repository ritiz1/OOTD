from django.urls import path

from .views import recommend_outfits


urlpatterns = [
    path("", recommend_outfits, name="recommend-outfits"),
]
