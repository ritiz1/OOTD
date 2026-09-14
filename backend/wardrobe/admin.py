from django.contrib import admin

from .models import (
    BottomAttributes,
    ClothingAnalysis,
    ClothingColorGroup,
    ClothingColorGroupItem,
    ClothingDetailGroup,
    ClothingDetailGroupItem,
    ClothingItem,
    ClothingMaterialGroup,
    ClothingMaterialGroupItem,
    ClothingPatternGroup,
    ClothingPatternGroupItem,
    ClothingPocketGroup,
    ClothingPocketGroupItem,
    ClothingStyleGroup,
    ClothingStyleGroupItem,
    ClothingSubcategory,
    ClothingType,
    Color,
    Detail,
    DressAttributes,
    FootwearAttributes,
    Material,
    OnePieceAttributes,
    OuterwearAttributes,
    Pattern,
    PocketType,
    Style,
    TopAttributes,
    VisualAttributes,
)


class ClothingColorGroupItemInline(admin.TabularInline):
    model = ClothingColorGroupItem
    extra = 0


class ClothingMaterialGroupItemInline(admin.TabularInline):
    model = ClothingMaterialGroupItem
    extra = 0


class ClothingPatternGroupItemInline(admin.TabularInline):
    model = ClothingPatternGroupItem
    extra = 0


class ClothingDetailGroupItemInline(admin.TabularInline):
    model = ClothingDetailGroupItem
    extra = 0


class ClothingStyleGroupItemInline(admin.TabularInline):
    model = ClothingStyleGroupItem
    extra = 0


class ClothingPocketGroupItemInline(admin.TabularInline):
    model = ClothingPocketGroupItem
    extra = 0


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("name", "hex_value")
    search_fields = ("name",)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Pattern)
class PatternAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(PocketType)
class PocketTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ClothingSubcategory)
class ClothingSubcategoryAdmin(admin.ModelAdmin):
    list_display = ("type_name", "name")
    list_filter = ("type_name",)
    search_fields = ("name",)


@admin.register(TopAttributes)
class TopAttributesAdmin(admin.ModelAdmin):
    list_display = ("id", "sleeve_length", "fit", "length")


@admin.register(BottomAttributes)
class BottomAttributesAdmin(admin.ModelAdmin):
    list_display = ("id", "rise", "leg_shape", "fit", "length")


@admin.register(DressAttributes)
class DressAttributesAdmin(admin.ModelAdmin):
    list_display = ("id", "silhouette", "dress_length", "fit")


@admin.register(OuterwearAttributes)
class OuterwearAttributesAdmin(admin.ModelAdmin):
    list_display = ("id", "jacket_length", "fit", "insulation")


@admin.register(FootwearAttributes)
class FootwearAttributesAdmin(admin.ModelAdmin):
    list_display = ("id", "shoe_height", "heel_type", "shoe_profile")


@admin.register(OnePieceAttributes)
class OnePieceAttributesAdmin(admin.ModelAdmin):
    list_display = ("id", "leg_shape", "length", "fit")


@admin.register(ClothingType)
class ClothingTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "subcategory")
    list_filter = ("name",)
    search_fields = ("subcategory__name",)
    autocomplete_fields = ("subcategory",)


@admin.register(ClothingColorGroup)
class ClothingColorGroupAdmin(admin.ModelAdmin):
    inlines = [ClothingColorGroupItemInline]


@admin.register(ClothingMaterialGroup)
class ClothingMaterialGroupAdmin(admin.ModelAdmin):
    inlines = [ClothingMaterialGroupItemInline]


@admin.register(ClothingPatternGroup)
class ClothingPatternGroupAdmin(admin.ModelAdmin):
    inlines = [ClothingPatternGroupItemInline]


@admin.register(ClothingDetailGroup)
class ClothingDetailGroupAdmin(admin.ModelAdmin):
    inlines = [ClothingDetailGroupItemInline]


@admin.register(ClothingStyleGroup)
class ClothingStyleGroupAdmin(admin.ModelAdmin):
    inlines = [ClothingStyleGroupItemInline]


@admin.register(ClothingPocketGroup)
class ClothingPocketGroupAdmin(admin.ModelAdmin):
    inlines = [ClothingPocketGroupItemInline]


@admin.register(VisualAttributes)
class VisualAttributesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "brightness",
        "saturation",
        "visual_complexity",
        "statement_level",
    )


@admin.register(ClothingAnalysis)
class ClothingAnalysisAdmin(admin.ModelAdmin):
    list_display = ("id", "model_name", "model_version", "overall_confidence", "created_at")
    list_filter = ("model_name",)
    search_fields = ("model_name", "model_version")


@admin.register(ClothingItem)
class ClothingItemAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "type", "created_at", "updated_at")
    list_filter = ("type__name", "created_at")
    search_fields = ("user__email", "image_url")
    autocomplete_fields = ("user", "type")
    readonly_fields = ("created_at", "updated_at")
