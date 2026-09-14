from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from .attributes import (
    BottomAttributes,
    DressAttributes,
    FootwearAttributes,
    OnePieceAttributes,
    OuterwearAttributes,
    TopAttributes,
)
from .choices import (
    Brightness,
    ClothingTypeName,
    Saturation,
    StatementLevel,
    Structure,
    SurfaceFinish,
    Symmetry,
    Transparency,
    VisualComplexity,
)
from .groups import (
    ClothingColorGroup,
    ClothingDetailGroup,
    ClothingMaterialGroup,
    ClothingPatternGroup,
    ClothingPocketGroup,
    ClothingStyleGroup,
)
from .lookups import ClothingSubcategory, UUIDModel


class VisualAttributes(UUIDModel):
    dominant_color_hex = models.CharField(max_length=7, blank=True, default="")
    brightness = models.CharField(max_length=32, choices=Brightness.choices)
    saturation = models.CharField(max_length=32, choices=Saturation.choices)
    visual_complexity = models.CharField(max_length=32, choices=VisualComplexity.choices)
    statement_level = models.CharField(max_length=32, choices=StatementLevel.choices)
    structure = models.CharField(max_length=32, choices=Structure.choices)
    surface_finish = models.CharField(max_length=32, choices=SurfaceFinish.choices)
    transparency = models.CharField(max_length=32, choices=Transparency.choices)
    symmetry = models.CharField(max_length=32, choices=Symmetry.choices)

    class Meta:
        verbose_name_plural = "visual attributes"

    def __str__(self):
        return f"VisualAttributes({self.pk})"


class ClothingAnalysis(UUIDModel):
    model_name = models.CharField(max_length=128)
    model_version = models.CharField(max_length=64, blank=True, default="")
    raw_response = models.JSONField(default=dict)
    overall_confidence = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "clothing analyses"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.model_name} ({self.overall_confidence})"


ATTRIBUTE_FK_FIELDS = (
    "top_attributes",
    "bottom_attributes",
    "dress_attributes",
    "outerwear_attributes",
    "footwear_attributes",
    "one_piece_attributes",
)

TYPE_TO_ATTRIBUTE_FIELD = {
    ClothingTypeName.TOP: "top_attributes",
    ClothingTypeName.BOTTOM: "bottom_attributes",
    ClothingTypeName.DRESS: "dress_attributes",
    ClothingTypeName.OUTERWEAR: "outerwear_attributes",
    ClothingTypeName.FOOTWEAR: "footwear_attributes",
    ClothingTypeName.ONE_PIECE: "one_piece_attributes",
}


class ClothingType(UUIDModel):
    name = models.CharField(max_length=32, choices=ClothingTypeName.choices)
    subcategory = models.ForeignKey(
        ClothingSubcategory,
        on_delete=models.PROTECT,
        related_name="clothing_types",
    )
    top_attributes = models.OneToOneField(
        TopAttributes,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="clothing_type",
    )
    bottom_attributes = models.OneToOneField(
        BottomAttributes,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="clothing_type",
    )
    dress_attributes = models.OneToOneField(
        DressAttributes,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="clothing_type",
    )
    outerwear_attributes = models.OneToOneField(
        OuterwearAttributes,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="clothing_type",
    )
    footwear_attributes = models.OneToOneField(
        FootwearAttributes,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="clothing_type",
    )
    one_piece_attributes = models.OneToOneField(
        OnePieceAttributes,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="clothing_type",
    )

    class Meta:
        verbose_name = "clothing type"
        constraints = [
            models.CheckConstraint(
                name="wardrobe_clothingtype_exactly_one_attribute",
                condition=(
                    Q(
                        top_attributes__isnull=False,
                        bottom_attributes__isnull=True,
                        dress_attributes__isnull=True,
                        outerwear_attributes__isnull=True,
                        footwear_attributes__isnull=True,
                        one_piece_attributes__isnull=True,
                    )
                    | Q(
                        top_attributes__isnull=True,
                        bottom_attributes__isnull=False,
                        dress_attributes__isnull=True,
                        outerwear_attributes__isnull=True,
                        footwear_attributes__isnull=True,
                        one_piece_attributes__isnull=True,
                    )
                    | Q(
                        top_attributes__isnull=True,
                        bottom_attributes__isnull=True,
                        dress_attributes__isnull=False,
                        outerwear_attributes__isnull=True,
                        footwear_attributes__isnull=True,
                        one_piece_attributes__isnull=True,
                    )
                    | Q(
                        top_attributes__isnull=True,
                        bottom_attributes__isnull=True,
                        dress_attributes__isnull=True,
                        outerwear_attributes__isnull=False,
                        footwear_attributes__isnull=True,
                        one_piece_attributes__isnull=True,
                    )
                    | Q(
                        top_attributes__isnull=True,
                        bottom_attributes__isnull=True,
                        dress_attributes__isnull=True,
                        outerwear_attributes__isnull=True,
                        footwear_attributes__isnull=False,
                        one_piece_attributes__isnull=True,
                    )
                    | Q(
                        top_attributes__isnull=True,
                        bottom_attributes__isnull=True,
                        dress_attributes__isnull=True,
                        outerwear_attributes__isnull=True,
                        footwear_attributes__isnull=True,
                        one_piece_attributes__isnull=False,
                    )
                ),
            )
        ]

    def clean(self):
        super().clean()
        populated = [field for field in ATTRIBUTE_FK_FIELDS if getattr(self, f"{field}_id")]
        if len(populated) != 1:
            raise ValidationError(
                "Exactly one type-attribute relation must be set on ClothingType."
            )
        expected = TYPE_TO_ATTRIBUTE_FIELD.get(self.name)
        if expected and populated[0] != expected:
            raise ValidationError(
                {
                    expected: (
                        f"For type '{self.name}', only '{expected}' may be set "
                        f"(got '{populated[0]}')."
                    )
                }
            )
        if self.subcategory_id and self.subcategory.type_name != self.name:
            raise ValidationError(
                {
                    "subcategory": (
                        f"Subcategory type_name '{self.subcategory.type_name}' "
                        f"does not match clothing type '{self.name}'."
                    )
                }
            )

    @property
    def attributes(self):
        for field in ATTRIBUTE_FK_FIELDS:
            value = getattr(self, field)
            if value is not None:
                return value
        return None

    def __str__(self):
        return f"{self.name}/{self.subcategory.name if self.subcategory_id else '?'}"


class ClothingItem(UUIDModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clothing_items",
    )
    image_url = models.TextField()
    type = models.ForeignKey(
        ClothingType,
        on_delete=models.PROTECT,
        related_name="clothing_items",
    )
    color_group = models.OneToOneField(
        ClothingColorGroup,
        on_delete=models.CASCADE,
        related_name="clothing_item",
    )
    material_group = models.OneToOneField(
        ClothingMaterialGroup,
        on_delete=models.CASCADE,
        related_name="clothing_item",
    )
    pattern_group = models.OneToOneField(
        ClothingPatternGroup,
        on_delete=models.CASCADE,
        related_name="clothing_item",
    )
    detail_group = models.OneToOneField(
        ClothingDetailGroup,
        on_delete=models.CASCADE,
        related_name="clothing_item",
    )
    style_group = models.OneToOneField(
        ClothingStyleGroup,
        on_delete=models.CASCADE,
        related_name="clothing_item",
    )
    pocket_group = models.OneToOneField(
        ClothingPocketGroup,
        on_delete=models.CASCADE,
        related_name="clothing_item",
    )
    visual_attributes = models.OneToOneField(
        VisualAttributes,
        on_delete=models.CASCADE,
        related_name="clothing_item",
    )
    analysis = models.OneToOneField(
        ClothingAnalysis,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clothing_item",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "clothing item"

    def __str__(self):
        return f"ClothingItem({self.pk})"
