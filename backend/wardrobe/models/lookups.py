import uuid

from django.db import models

from .choices import (
    ClothingTypeName,
    ColorName,
    DetailName,
    MaterialName,
    PatternName,
    PocketTypeName,
    StyleName,
)


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class ClothingSubcategory(UUIDModel):
    type_name = models.CharField(max_length=32, choices=ClothingTypeName.choices)
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "clothing subcategories"
        constraints = [
            models.UniqueConstraint(
                fields=["type_name", "name"],
                name="wardrobe_subcategory_type_name_unique",
            )
        ]
        ordering = ["type_name", "name"]

    def __str__(self):
        return f"{self.type_name}:{self.name}"


class Color(UUIDModel):
    name = models.CharField(max_length=32, choices=ColorName.choices, unique=True)
    hex_value = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Material(UUIDModel):
    name = models.CharField(max_length=32, choices=MaterialName.choices, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Pattern(UUIDModel):
    name = models.CharField(max_length=32, choices=PatternName.choices, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Detail(UUIDModel):
    name = models.CharField(max_length=32, choices=DetailName.choices, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "details"

    def __str__(self):
        return self.name


class Style(UUIDModel):
    name = models.CharField(max_length=32, choices=StyleName.choices, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class PocketType(UUIDModel):
    name = models.CharField(max_length=32, choices=PocketTypeName.choices, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
