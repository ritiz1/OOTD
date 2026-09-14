from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .choices import ColorRole, PatternDensity, PatternOrientation, PatternScale
from .lookups import Color, Detail, Material, Pattern, PocketType, Style, UUIDModel


class ClothingColorGroup(UUIDModel):
    class Meta:
        verbose_name = "clothing color group"
        verbose_name_plural = "clothing color groups"

    def __str__(self):
        return f"ColorGroup({self.pk})"


class ClothingColorGroupItem(UUIDModel):
    group = models.ForeignKey(
        ClothingColorGroup,
        on_delete=models.CASCADE,
        related_name="items",
    )
    color = models.ForeignKey(Color, on_delete=models.PROTECT, related_name="group_items")
    role = models.CharField(max_length=16, choices=ColorRole.choices)
    percentage = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    class Meta:
        verbose_name = "clothing color group item"
        ordering = ["role", "color__name"]

    def __str__(self):
        return f"{self.color} ({self.role})"


class ClothingMaterialGroup(UUIDModel):
    class Meta:
        verbose_name = "clothing material group"
        verbose_name_plural = "clothing material groups"

    def __str__(self):
        return f"MaterialGroup({self.pk})"


class ClothingMaterialGroupItem(UUIDModel):
    group = models.ForeignKey(
        ClothingMaterialGroup,
        on_delete=models.CASCADE,
        related_name="items",
    )
    material = models.ForeignKey(
        Material,
        on_delete=models.PROTECT,
        related_name="group_items",
    )
    percentage = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    class Meta:
        verbose_name = "clothing material group item"
        ordering = ["material__name"]

    def __str__(self):
        return str(self.material)


class ClothingPatternGroup(UUIDModel):
    class Meta:
        verbose_name = "clothing pattern group"
        verbose_name_plural = "clothing pattern groups"

    def __str__(self):
        return f"PatternGroup({self.pk})"


class ClothingPatternGroupItem(UUIDModel):
    group = models.ForeignKey(
        ClothingPatternGroup,
        on_delete=models.CASCADE,
        related_name="items",
    )
    pattern = models.ForeignKey(
        Pattern,
        on_delete=models.PROTECT,
        related_name="group_items",
    )
    scale = models.CharField(max_length=16, choices=PatternScale.choices)
    density = models.CharField(max_length=16, choices=PatternDensity.choices)
    orientation = models.CharField(max_length=16, choices=PatternOrientation.choices)

    class Meta:
        verbose_name = "clothing pattern group item"
        ordering = ["pattern__name"]

    def __str__(self):
        return str(self.pattern)


class ClothingDetailGroup(UUIDModel):
    class Meta:
        verbose_name = "clothing detail group"
        verbose_name_plural = "clothing detail groups"

    def __str__(self):
        return f"DetailGroup({self.pk})"


class ClothingDetailGroupItem(UUIDModel):
    group = models.ForeignKey(
        ClothingDetailGroup,
        on_delete=models.CASCADE,
        related_name="items",
    )
    detail = models.ForeignKey(Detail, on_delete=models.PROTECT, related_name="group_items")

    class Meta:
        verbose_name = "clothing detail group item"
        ordering = ["detail__name"]

    def __str__(self):
        return str(self.detail)


class ClothingStyleGroup(UUIDModel):
    class Meta:
        verbose_name = "clothing style group"
        verbose_name_plural = "clothing style groups"

    def __str__(self):
        return f"StyleGroup({self.pk})"


class ClothingStyleGroupItem(UUIDModel):
    group = models.ForeignKey(
        ClothingStyleGroup,
        on_delete=models.CASCADE,
        related_name="items",
    )
    style = models.ForeignKey(Style, on_delete=models.PROTECT, related_name="group_items")
    confidence = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "clothing style group item"
        ordering = ["-confidence", "style__name"]

    def __str__(self):
        return str(self.style)


class ClothingPocketGroup(UUIDModel):
    class Meta:
        verbose_name = "clothing pocket group"
        verbose_name_plural = "clothing pocket groups"

    def __str__(self):
        return f"PocketGroup({self.pk})"


class ClothingPocketGroupItem(UUIDModel):
    group = models.ForeignKey(
        ClothingPocketGroup,
        on_delete=models.CASCADE,
        related_name="items",
    )
    pocket_type = models.ForeignKey(
        PocketType,
        on_delete=models.PROTECT,
        related_name="group_items",
    )
    count = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = "clothing pocket group item"
        ordering = ["pocket_type__name"]

    def __str__(self):
        return f"{self.pocket_type} x{self.count}"
