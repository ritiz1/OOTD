from django.db import models

from .choices import (
    BackStyle,
    BottomClosureType,
    BottomFit,
    BottomLength,
    ClosureType,
    CollarType,
    DressLength,
    HeelHeight,
    HeelType,
    HemStyle,
    HoodType,
    Insulation,
    JacketLength,
    LapelType,
    LegShape,
    Neckline,
    Rise,
    ShoeClosure,
    ShoeHeight,
    ShoeProfile,
    ShoulderStyle,
    Silhouette,
    SleeveLength,
    SleeveType,
    SoleType,
    StrapType,
    ToeShape,
    TopFit,
    TopLength,
    WaistStyle,
    WaistbandType,
)
from .lookups import UUIDModel


class TopAttributes(UUIDModel):
    sleeve_length = models.CharField(max_length=32, choices=SleeveLength.choices)
    sleeve_type = models.CharField(max_length=32, choices=SleeveType.choices)
    neckline = models.CharField(max_length=32, choices=Neckline.choices)
    collar_type = models.CharField(max_length=32, choices=CollarType.choices)
    shoulder_style = models.CharField(max_length=32, choices=ShoulderStyle.choices)
    hem_style = models.CharField(max_length=32, choices=HemStyle.choices)
    closure_type = models.CharField(max_length=32, choices=ClosureType.choices)
    hood_type = models.CharField(max_length=32, choices=HoodType.choices)
    fit = models.CharField(max_length=32, choices=TopFit.choices)
    length = models.CharField(max_length=32, choices=TopLength.choices)

    class Meta:
        verbose_name_plural = "top attributes"

    def __str__(self):
        return f"TopAttributes({self.pk})"


class BottomAttributes(UUIDModel):
    rise = models.CharField(max_length=32, choices=Rise.choices)
    leg_shape = models.CharField(max_length=32, choices=LegShape.choices)
    waistband_type = models.CharField(max_length=32, choices=WaistbandType.choices)
    hem_style = models.CharField(max_length=32, choices=HemStyle.choices)
    closure_type = models.CharField(max_length=32, choices=BottomClosureType.choices)
    fit = models.CharField(max_length=32, choices=BottomFit.choices)
    length = models.CharField(max_length=32, choices=BottomLength.choices)

    class Meta:
        verbose_name_plural = "bottom attributes"

    def __str__(self):
        return f"BottomAttributes({self.pk})"


class DressAttributes(UUIDModel):
    sleeve_length = models.CharField(max_length=32, choices=SleeveLength.choices)
    sleeve_type = models.CharField(max_length=32, choices=SleeveType.choices)
    neckline = models.CharField(max_length=32, choices=Neckline.choices)
    strap_type = models.CharField(max_length=32, choices=StrapType.choices)
    silhouette = models.CharField(max_length=32, choices=Silhouette.choices)
    dress_length = models.CharField(max_length=32, choices=DressLength.choices)
    back_style = models.CharField(max_length=32, choices=BackStyle.choices)
    closure_type = models.CharField(max_length=32, choices=ClosureType.choices)
    fit = models.CharField(max_length=32, choices=TopFit.choices)

    class Meta:
        verbose_name_plural = "dress attributes"

    def __str__(self):
        return f"DressAttributes({self.pk})"


class OuterwearAttributes(UUIDModel):
    sleeve_length = models.CharField(max_length=32, choices=SleeveLength.choices)
    collar_type = models.CharField(max_length=32, choices=CollarType.choices)
    lapel_type = models.CharField(max_length=32, choices=LapelType.choices)
    closure_type = models.CharField(max_length=32, choices=ClosureType.choices)
    hood_type = models.CharField(max_length=32, choices=HoodType.choices)
    jacket_length = models.CharField(max_length=32, choices=JacketLength.choices)
    fit = models.CharField(max_length=32, choices=TopFit.choices)
    insulation = models.CharField(max_length=32, choices=Insulation.choices)

    class Meta:
        verbose_name_plural = "outerwear attributes"

    def __str__(self):
        return f"OuterwearAttributes({self.pk})"


class FootwearAttributes(UUIDModel):
    shoe_height = models.CharField(max_length=32, choices=ShoeHeight.choices)
    toe_shape = models.CharField(max_length=32, choices=ToeShape.choices)
    heel_type = models.CharField(max_length=32, choices=HeelType.choices)
    heel_height = models.CharField(max_length=32, choices=HeelHeight.choices)
    shoe_closure = models.CharField(max_length=32, choices=ShoeClosure.choices)
    sole_type = models.CharField(max_length=32, choices=SoleType.choices)
    shoe_profile = models.CharField(max_length=32, choices=ShoeProfile.choices)

    class Meta:
        verbose_name_plural = "footwear attributes"

    def __str__(self):
        return f"FootwearAttributes({self.pk})"


class OnePieceAttributes(UUIDModel):
    sleeve_length = models.CharField(max_length=32, choices=SleeveLength.choices)
    sleeve_type = models.CharField(max_length=32, choices=SleeveType.choices)
    neckline = models.CharField(max_length=32, choices=Neckline.choices)
    collar_type = models.CharField(max_length=32, choices=CollarType.choices)
    leg_shape = models.CharField(max_length=32, choices=LegShape.choices)
    length = models.CharField(max_length=32, choices=BottomLength.choices)
    waist_style = models.CharField(max_length=32, choices=WaistStyle.choices)
    closure_type = models.CharField(max_length=32, choices=ClosureType.choices)
    fit = models.CharField(max_length=32, choices=TopFit.choices)

    class Meta:
        verbose_name_plural = "one piece attributes"

    def __str__(self):
        return f"OnePieceAttributes({self.pk})"
