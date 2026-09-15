from django.urls import path

from .views.desc_view import describe_clothing_item
from .views.recommend_view import recommend_outfits

urlpatterns = [
    path("describe/", describe_clothing_item, name="describe_clothing_item"),
    path("recommend/", recommend_outfits, name="recommend_outfits"),
]
