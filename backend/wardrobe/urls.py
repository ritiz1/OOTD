from django.urls import path

from .views.desc_view import describe_clothing_item

urlpatterns = [
    path("describe/", describe_clothing_item, name="describe_clothing_item"),
]
