from django.urls import path

from .views.desc_view import describe_clothing_item
from .views.item_view import clothing_item_detail, clothing_item_list
from .views.recommend_view import recommend_outfits

urlpatterns = [
    path("describe/", describe_clothing_item, name="describe_clothing_item"),
    path("items/", clothing_item_list, name="clothing_item_list"),
    path("items/<uuid:item_id>/", clothing_item_detail, name="clothing_item_detail"),
    path("recommend/", recommend_outfits, name="recommend_outfits"),
]
