"""WearThis image-description agent.

The application passes an image (uploaded bytes or a URL represented as image
content) to this ADK agent.  The agent returns only the normalized metadata
needed to populate the clothing-item relationship described in
WEARTHIS_Clothing_Database_Model.md.  Persistence, uploads, and HTTP endpoints
intentionally live outside this module.
"""

from __future__ import annotations

import os
from typing import Annotated, Literal, Union

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from pydantic import BaseModel, ConfigDict, Field


# LiteLLM deliberately does not load .env in ADK production mode.  Loading the
# backend .env here lets a future caller simply set GEMINI_API_KEY there.
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


class StrictModel(BaseModel):
    """Reject fields that are not part of the WearThis database model."""

    model_config = ConfigDict(extra="forbid")


ColorName = Literal[
    "black", "white", "gray", "charcoal", "silver", "cream", "ivory",
    "beige", "tan", "khaki", "camel", "brown", "red", "burgundy",
    "maroon", "pink", "rose", "orange", "coral", "peach", "yellow",
    "gold", "mustard", "green", "lime", "olive", "sage", "mint",
    "emerald", "forest_green", "blue", "navy", "royal_blue", "sky_blue",
    "baby_blue", "teal", "turquoise", "purple", "lavender", "violet",
    "plum", "multicolor", "transparent", "unknown",
]
MaterialName = Literal[
    "cotton", "organic_cotton", "denim", "linen", "wool", "merino_wool",
    "cashmere", "silk", "satin", "velvet", "corduroy", "leather",
    "faux_leather", "suede", "faux_suede", "polyester", "nylon", "acrylic",
    "spandex", "elastane", "rayon", "viscose", "modal", "fleece", "jersey",
    "canvas", "mesh", "lace", "chiffon", "tweed", "rubber", "synthetic",
    "mixed", "unknown",
]


class Color(StrictModel):
    name: ColorName
    role: Literal["primary", "secondary", "accent"]
    percentage: Annotated[float | None, Field(ge=0, le=100)] = None


class Material(StrictModel):
    name: MaterialName
    percentage: Annotated[float | None, Field(ge=0, le=100)] = None


class Pattern(StrictModel):
    name: Literal[
        "none", "solid", "striped", "checked", "plaid", "gingham",
        "polka_dot", "floral", "animal_print", "camouflage", "geometric",
        "abstract", "paisley", "tie_dye", "gradient", "ombre", "color_block",
        "graphic", "logo", "text", "other",
    ]
    scale: Literal["none", "small", "medium", "large", "mixed"]
    density: Literal["none", "sparse", "medium", "dense"]
    orientation: Literal["none", "horizontal", "vertical", "diagonal", "mixed"]


class Style(StrictModel):
    name: Literal[
        "minimalist", "classic", "casual", "smart_casual", "business_casual",
        "formal", "preppy", "old_money", "quiet_luxury", "streetwear", "urban",
        "skater", "sporty", "athleisure", "workwear", "utility", "military",
        "outdoorsy", "gorpcore", "techwear", "vintage", "retro", "y2k",
        "bohemian", "romantic", "western", "grunge", "punk", "gothic", "edgy",
        "avant_garde",
    ]
    confidence: Annotated[float | None, Field(ge=0, le=1)] = None


class Pocket(StrictModel):
    name: Literal[
        "side", "slash", "patch", "chest", "cargo", "welt", "zippered",
        "kangaroo", "back", "coin", "hidden", "flap",
    ]
    count: Annotated[int, Field(ge=1)]


SleeveLength = Literal["none", "sleeveless", "cap", "short", "elbow", "three_quarter", "long", "extra_long"]
SleeveType = Literal["none", "regular", "raglan", "set_in", "drop_shoulder", "puff", "bell", "bishop", "batwing", "flutter", "rolled"]
Neckline = Literal["none", "crew", "round", "v_neck", "deep_v", "square", "scoop", "boat", "halter", "sweetheart", "turtleneck", "mock_neck", "off_shoulder", "one_shoulder", "henley"]
CollarType = Literal["none", "shirt", "spread", "point", "button_down", "mandarin", "polo", "camp", "peter_pan", "shawl", "notched", "stand"]
TopClosure = Literal["none", "pullover", "buttons", "zipper", "half_zip", "quarter_zip", "snap", "hook_and_eye", "tie"]
HoodType = Literal["none", "fixed", "detachable", "oversized", "drawstring"]
TopFit = Literal["skinny", "slim", "fitted", "regular", "relaxed", "oversized", "boxy"]
LegShape = Literal["none", "skinny", "slim", "straight", "tapered", "wide", "flare", "bootcut", "baggy", "carrot"]
BottomLength = Literal["micro", "short", "knee", "below_knee", "cropped", "ankle", "full", "floor"]
HemStyle = Literal["none", "straight", "curved", "rounded", "asymmetric", "cropped", "ribbed", "raw", "split"]


class TopAttributes(StrictModel):
    sleeve_length: SleeveLength
    sleeve_type: SleeveType
    neckline: Neckline
    collar_type: CollarType
    shoulder_style: Literal["none", "regular", "drop_shoulder", "raglan", "structured", "padded", "off_shoulder", "one_shoulder"]
    hem_style: HemStyle
    closure_type: TopClosure
    hood_type: HoodType
    fit: TopFit
    length: Literal["cropped", "waist", "hip", "longline", "oversized_long"]


class BottomAttributes(StrictModel):
    rise: Literal["none", "low", "mid", "high", "ultra_high"]
    leg_shape: LegShape
    waistband_type: Literal["none", "standard", "elastic", "drawstring", "belted", "ribbed", "foldover"]
    hem_style: HemStyle
    closure_type: Literal["none", "zip_fly", "button_fly", "buttons", "drawstring", "elastic", "hook_and_bar", "side_zip"]
    fit: Literal["skinny", "slim", "regular", "relaxed", "loose", "baggy", "oversized"]
    length: BottomLength


class DressAttributes(StrictModel):
    sleeve_length: SleeveLength
    sleeve_type: SleeveType
    neckline: Neckline
    strap_type: Literal["none", "strapless", "spaghetti", "thin", "medium", "wide", "halter", "one_shoulder"]
    silhouette: Literal["straight", "a_line", "bodycon", "fit_and_flare", "empire", "shift", "sheath", "wrap", "slip", "ball_gown", "mermaid"]
    dress_length: Literal["mini", "above_knee", "knee", "midi", "maxi", "floor"]
    back_style: Literal["closed", "open_back", "low_back", "cross_back", "racerback", "keyhole", "lace_up"]
    closure_type: TopClosure
    fit: TopFit


class OuterwearAttributes(StrictModel):
    sleeve_length: SleeveLength
    collar_type: CollarType
    lapel_type: Literal["none", "notch", "peak", "shawl"]
    closure_type: TopClosure
    hood_type: HoodType
    jacket_length: Literal["cropped", "waist", "hip", "mid_thigh", "knee", "below_knee", "full_length"]
    fit: TopFit
    insulation: Literal["none", "light", "medium", "heavy", "padded", "down", "fleece_lined"]


class FootwearAttributes(StrictModel):
    shoe_height: Literal["low", "ankle", "mid", "high", "knee", "over_knee"]
    toe_shape: Literal["round", "almond", "square", "pointed", "open", "wide"]
    heel_type: Literal["none", "flat", "block", "stiletto", "kitten", "wedge", "platform", "cone"]
    heel_height: Literal["none", "flat", "low", "medium", "high", "very_high"]
    shoe_closure: Literal["none", "slip_on", "laces", "zipper", "buckle", "velcro", "strap", "elastic"]
    sole_type: Literal["flat", "rubber", "foam", "leather", "lug", "platform", "chunky", "crepe"]
    shoe_profile: Literal["minimal", "standard", "chunky", "sleek", "athletic", "rugged"]


class OnePieceAttributes(StrictModel):
    sleeve_length: SleeveLength
    sleeve_type: SleeveType
    neckline: Neckline
    collar_type: CollarType
    leg_shape: LegShape
    length: BottomLength
    waist_style: Literal["none", "natural", "high", "low", "elastic", "drawstring", "belted", "fitted"]
    closure_type: TopClosure
    fit: TopFit


class Top(StrictModel):
    name: Literal["top"]
    subcategory: Literal["t_shirt", "shirt", "button_up", "polo", "tank_top", "crop_top", "blouse", "sweater", "sweatshirt", "hoodie", "cardigan", "jersey", "vest", "turtleneck", "other"]
    attributes: TopAttributes


class Bottom(StrictModel):
    name: Literal["bottom"]
    subcategory: Literal["jeans", "trousers", "chinos", "shorts", "sweatpants", "joggers", "leggings", "skirt", "cargo_pants", "dress_pants", "track_pants", "other"]
    attributes: BottomAttributes


class Dress(StrictModel):
    name: Literal["dress"]
    subcategory: Literal["mini_dress", "midi_dress", "maxi_dress", "shirt_dress", "bodycon_dress", "wrap_dress", "slip_dress", "sundress", "cocktail_dress", "formal_dress", "other"]
    attributes: DressAttributes


class Outerwear(StrictModel):
    name: Literal["outerwear"]
    subcategory: Literal["jacket", "coat", "blazer", "denim_jacket", "leather_jacket", "bomber_jacket", "puffer_jacket", "windbreaker", "rain_jacket", "trench_coat", "parka", "overcoat", "other"]
    attributes: OuterwearAttributes


class Footwear(StrictModel):
    name: Literal["footwear"]
    subcategory: Literal["sneakers", "running_shoes", "boots", "ankle_boots", "dress_shoes", "loafers", "oxfords", "sandals", "slides", "heels", "flats", "slippers", "other"]
    attributes: FootwearAttributes


class OnePiece(StrictModel):
    name: Literal["one_piece"]
    subcategory: Literal["jumpsuit", "romper", "overalls", "bodysuit", "tracksuit", "other"]
    attributes: OnePieceAttributes


ClothingType = Annotated[Union[Top, Bottom, Dress, Outerwear, Footwear, OnePiece], Field(discriminator="name")]


class VisualAttributes(StrictModel):
    dominant_color_hex: Annotated[str, Field(pattern=r"^#[0-9A-Fa-f]{6}$")]
    brightness: Literal["very_dark", "dark", "medium", "light", "very_light"]
    saturation: Literal["desaturated", "muted", "medium", "vibrant", "highly_vibrant"]
    visual_complexity: Literal["very_simple", "simple", "moderate", "busy", "very_busy"]
    statement_level: Literal["basic", "subtle", "moderate", "statement", "bold"]
    structure: Literal["soft", "semi_structured", "structured", "rigid"]
    surface_finish: Literal["matte", "semi_matte", "semi_gloss", "glossy", "metallic", "sparkly"]
    transparency: Literal["opaque", "slightly_sheer", "sheer", "transparent"]
    symmetry: Literal["symmetric", "mostly_symmetric", "asymmetric"]


class ClothingDescription(StrictModel):
    """JSON payload that maps to the metadata tables linked by clothing_items."""

    type: ClothingType
    colors: list[Color]
    materials: list[Material]
    patterns: list[Pattern]
    details: list[Literal[
        "embroidery", "sequins", "beading", "rhinestones", "studs", "fringe",
        "tassels", "ruffles", "bows", "lace", "patches", "applique",
        "distressing", "rips", "cutouts", "pleats", "gathers", "smocking",
        "quilting", "contrast_stitching", "piping", "chains", "buckles",
        "visible_buttons", "visible_zippers", "logo", "graphic", "text",
    ]]
    styles: list[Style]
    pockets: list[Pocket]
    visual_attributes: VisualAttributes


INSTRUCTION = """
You are WearThis's clothing-image metadata extractor. Analyze exactly one clothing
item in the supplied image and return only a JSON value matching the output
schema. Do not describe the image in prose.

Use only the schema's enum values. Never add fields, comments, IDs, timestamps,
image URLs, database foreign keys, or values outside the enum. Pick `other` only
where that enum permits it. Use `unknown` for an unidentifiable color or material.
Use `none` for a conceptually applicable attribute that cannot be seen or does
not apply. Always emit every attribute in the selected type's attributes object.

CRITICAL: `type.name` is the database category, never a human clothing label.
It must be exactly one of `top`, `bottom`, `dress`, `outerwear`, `footwear`, or
`one_piece`. For example, a camel coat is `{ "name": "outerwear",
"subcategory": "coat", ... }`, not `{ "name": "Camel Coat", ... }`.
`type.subcategory` must likewise be one of the lowercase underscore-separated
values permitted by the schema for that category.

The arrays represent the database group-item rows: details and pockets must be
empty arrays when absent (never emit a fake `none` detail/pocket). For a plain
item, emit one pattern with name `solid` and scale, density, and orientation all
`none`. Estimate percentages only when visually defensible; otherwise use null.
Do not infer an exact fiber composition from appearance: use `unknown` when the
material cannot be reliably identified. `dominant_color_hex` must be an observed
six-digit hex color. Style confidences must be from 0 through 1.
""".strip()


def create_agent(model_name: str) -> Agent:
    """Create the description agent for one Gemini model in the fallback order."""

    return Agent(
        name="clothing_description_agent",
        description="Extracts database-constrained metadata from one clothing image.",
        model=LiteLlm(
            model=f"gemini/{model_name}",
            api_key=os.getenv("GEMINI_API_KEY"),
        ),
        instruction=INSTRUCTION,
        output_schema=ClothingDescription,
        output_key="clothing_description",
    )


# Retained for standalone agent tooling; API requests use create_agent() so they
# can select a retry/fallback model.
root_agent = create_agent(os.getenv("WEARTHIS_GEMINI_MODEL", "gemini-3.8-flash").removeprefix("gemini/"))
