from django.db import models


class ClothingTypeName(models.TextChoices):
    TOP = "top", "Top"
    BOTTOM = "bottom", "Bottom"
    DRESS = "dress", "Dress"
    OUTERWEAR = "outerwear", "Outerwear"
    FOOTWEAR = "footwear", "Footwear"
    ONE_PIECE = "one_piece", "One Piece"


class TopSubcategory(models.TextChoices):
    T_SHIRT = "t_shirt", "T-Shirt"
    SHIRT = "shirt", "Shirt"
    BUTTON_UP = "button_up", "Button Up"
    POLO = "polo", "Polo"
    TANK_TOP = "tank_top", "Tank Top"
    CROP_TOP = "crop_top", "Crop Top"
    BLOUSE = "blouse", "Blouse"
    SWEATER = "sweater", "Sweater"
    SWEATSHIRT = "sweatshirt", "Sweatshirt"
    HOODIE = "hoodie", "Hoodie"
    CARDIGAN = "cardigan", "Cardigan"
    JERSEY = "jersey", "Jersey"
    VEST = "vest", "Vest"
    TURTLENECK = "turtleneck", "Turtleneck"
    OTHER = "other", "Other"


class BottomSubcategory(models.TextChoices):
    JEANS = "jeans", "Jeans"
    TROUSERS = "trousers", "Trousers"
    CHINOS = "chinos", "Chinos"
    SHORTS = "shorts", "Shorts"
    SWEATPANTS = "sweatpants", "Sweatpants"
    JOGGERS = "joggers", "Joggers"
    LEGGINGS = "leggings", "Leggings"
    SKIRT = "skirt", "Skirt"
    CARGO_PANTS = "cargo_pants", "Cargo Pants"
    DRESS_PANTS = "dress_pants", "Dress Pants"
    TRACK_PANTS = "track_pants", "Track Pants"
    OTHER = "other", "Other"


class DressSubcategory(models.TextChoices):
    MINI_DRESS = "mini_dress", "Mini Dress"
    MIDI_DRESS = "midi_dress", "Midi Dress"
    MAXI_DRESS = "maxi_dress", "Maxi Dress"
    SHIRT_DRESS = "shirt_dress", "Shirt Dress"
    BODYCON_DRESS = "bodycon_dress", "Bodycon Dress"
    WRAP_DRESS = "wrap_dress", "Wrap Dress"
    SLIP_DRESS = "slip_dress", "Slip Dress"
    SUNDRESS = "sundress", "Sundress"
    COCKTAIL_DRESS = "cocktail_dress", "Cocktail Dress"
    FORMAL_DRESS = "formal_dress", "Formal Dress"
    OTHER = "other", "Other"


class OuterwearSubcategory(models.TextChoices):
    JACKET = "jacket", "Jacket"
    COAT = "coat", "Coat"
    BLAZER = "blazer", "Blazer"
    DENIM_JACKET = "denim_jacket", "Denim Jacket"
    LEATHER_JACKET = "leather_jacket", "Leather Jacket"
    BOMBER_JACKET = "bomber_jacket", "Bomber Jacket"
    PUFFER_JACKET = "puffer_jacket", "Puffer Jacket"
    WINDBREAKER = "windbreaker", "Windbreaker"
    RAIN_JACKET = "rain_jacket", "Rain Jacket"
    TRENCH_COAT = "trench_coat", "Trench Coat"
    PARKA = "parka", "Parka"
    OVERCOAT = "overcoat", "Overcoat"
    OTHER = "other", "Other"


class FootwearSubcategory(models.TextChoices):
    SNEAKERS = "sneakers", "Sneakers"
    RUNNING_SHOES = "running_shoes", "Running Shoes"
    BOOTS = "boots", "Boots"
    ANKLE_BOOTS = "ankle_boots", "Ankle Boots"
    DRESS_SHOES = "dress_shoes", "Dress Shoes"
    LOAFERS = "loafers", "Loafers"
    OXFORDS = "oxfords", "Oxfords"
    SANDALS = "sandals", "Sandals"
    SLIDES = "slides", "Slides"
    HEELS = "heels", "Heels"
    FLATS = "flats", "Flats"
    SLIPPERS = "slippers", "Slippers"
    OTHER = "other", "Other"


class OnePieceSubcategory(models.TextChoices):
    JUMPSUIT = "jumpsuit", "Jumpsuit"
    ROMPER = "romper", "Romper"
    OVERALLS = "overalls", "Overalls"
    BODYSUIT = "bodysuit", "Bodysuit"
    TRACKSUIT = "tracksuit", "Tracksuit"
    OTHER = "other", "Other"


class SleeveLength(models.TextChoices):
    NONE = "none", "None"
    SLEEVELESS = "sleeveless", "Sleeveless"
    CAP = "cap", "Cap"
    SHORT = "short", "Short"
    ELBOW = "elbow", "Elbow"
    THREE_QUARTER = "three_quarter", "Three Quarter"
    LONG = "long", "Long"
    EXTRA_LONG = "extra_long", "Extra Long"


class SleeveType(models.TextChoices):
    NONE = "none", "None"
    REGULAR = "regular", "Regular"
    RAGLAN = "raglan", "Raglan"
    SET_IN = "set_in", "Set In"
    DROP_SHOULDER = "drop_shoulder", "Drop Shoulder"
    PUFF = "puff", "Puff"
    BELL = "bell", "Bell"
    BISHOP = "bishop", "Bishop"
    BATWING = "batwing", "Batwing"
    FLUTTER = "flutter", "Flutter"
    ROLLED = "rolled", "Rolled"


class Neckline(models.TextChoices):
    NONE = "none", "None"
    CREW = "crew", "Crew"
    ROUND = "round", "Round"
    V_NECK = "v_neck", "V-Neck"
    DEEP_V = "deep_v", "Deep V"
    SQUARE = "square", "Square"
    SCOOP = "scoop", "Scoop"
    BOAT = "boat", "Boat"
    HALTER = "halter", "Halter"
    SWEETHEART = "sweetheart", "Sweetheart"
    TURTLENECK = "turtleneck", "Turtleneck"
    MOCK_NECK = "mock_neck", "Mock Neck"
    OFF_SHOULDER = "off_shoulder", "Off Shoulder"
    ONE_SHOULDER = "one_shoulder", "One Shoulder"
    HENLEY = "henley", "Henley"


class CollarType(models.TextChoices):
    NONE = "none", "None"
    SHIRT = "shirt", "Shirt"
    SPREAD = "spread", "Spread"
    POINT = "point", "Point"
    BUTTON_DOWN = "button_down", "Button Down"
    MANDARIN = "mandarin", "Mandarin"
    POLO = "polo", "Polo"
    CAMP = "camp", "Camp"
    PETER_PAN = "peter_pan", "Peter Pan"
    SHAWL = "shawl", "Shawl"
    NOTCHED = "notched", "Notched"
    STAND = "stand", "Stand"


class ShoulderStyle(models.TextChoices):
    NONE = "none", "None"
    REGULAR = "regular", "Regular"
    DROP_SHOULDER = "drop_shoulder", "Drop Shoulder"
    RAGLAN = "raglan", "Raglan"
    STRUCTURED = "structured", "Structured"
    PADDED = "padded", "Padded"
    OFF_SHOULDER = "off_shoulder", "Off Shoulder"
    ONE_SHOULDER = "one_shoulder", "One Shoulder"


class HemStyle(models.TextChoices):
    NONE = "none", "None"
    STRAIGHT = "straight", "Straight"
    CURVED = "curved", "Curved"
    ROUNDED = "rounded", "Rounded"
    ASYMMETRIC = "asymmetric", "Asymmetric"
    CROPPED = "cropped", "Cropped"
    RIBBED = "ribbed", "Ribbed"
    RAW = "raw", "Raw"
    SPLIT = "split", "Split"


class ClosureType(models.TextChoices):
    NONE = "none", "None"
    PULLOVER = "pullover", "Pullover"
    BUTTONS = "buttons", "Buttons"
    ZIPPER = "zipper", "Zipper"
    HALF_ZIP = "half_zip", "Half Zip"
    QUARTER_ZIP = "quarter_zip", "Quarter Zip"
    SNAP = "snap", "Snap"
    HOOK_AND_EYE = "hook_and_eye", "Hook and Eye"
    TIE = "tie", "Tie"


class HoodType(models.TextChoices):
    NONE = "none", "None"
    FIXED = "fixed", "Fixed"
    DETACHABLE = "detachable", "Detachable"
    OVERSIZED = "oversized", "Oversized"
    DRAWSTRING = "drawstring", "Drawstring"


class TopFit(models.TextChoices):
    SKINNY = "skinny", "Skinny"
    SLIM = "slim", "Slim"
    FITTED = "fitted", "Fitted"
    REGULAR = "regular", "Regular"
    RELAXED = "relaxed", "Relaxed"
    OVERSIZED = "oversized", "Oversized"
    BOXY = "boxy", "Boxy"


class TopLength(models.TextChoices):
    CROPPED = "cropped", "Cropped"
    WAIST = "waist", "Waist"
    HIP = "hip", "Hip"
    LONGLINE = "longline", "Longline"
    OVERSIZED_LONG = "oversized_long", "Oversized Long"


class Rise(models.TextChoices):
    NONE = "none", "None"
    LOW = "low", "Low"
    MID = "mid", "Mid"
    HIGH = "high", "High"
    ULTRA_HIGH = "ultra_high", "Ultra High"


class LegShape(models.TextChoices):
    NONE = "none", "None"
    SKINNY = "skinny", "Skinny"
    SLIM = "slim", "Slim"
    STRAIGHT = "straight", "Straight"
    TAPERED = "tapered", "Tapered"
    WIDE = "wide", "Wide"
    FLARE = "flare", "Flare"
    BOOTCUT = "bootcut", "Bootcut"
    BAGGY = "baggy", "Baggy"
    CARROT = "carrot", "Carrot"


class WaistbandType(models.TextChoices):
    NONE = "none", "None"
    STANDARD = "standard", "Standard"
    ELASTIC = "elastic", "Elastic"
    DRAWSTRING = "drawstring", "Drawstring"
    BELTED = "belted", "Belted"
    RIBBED = "ribbed", "Ribbed"
    FOLDOVER = "foldover", "Foldover"


class BottomClosureType(models.TextChoices):
    NONE = "none", "None"
    ZIP_FLY = "zip_fly", "Zip Fly"
    BUTTON_FLY = "button_fly", "Button Fly"
    BUTTONS = "buttons", "Buttons"
    DRAWSTRING = "drawstring", "Drawstring"
    ELASTIC = "elastic", "Elastic"
    HOOK_AND_BAR = "hook_and_bar", "Hook and Bar"
    SIDE_ZIP = "side_zip", "Side Zip"


class BottomFit(models.TextChoices):
    SKINNY = "skinny", "Skinny"
    SLIM = "slim", "Slim"
    REGULAR = "regular", "Regular"
    RELAXED = "relaxed", "Relaxed"
    LOOSE = "loose", "Loose"
    BAGGY = "baggy", "Baggy"
    OVERSIZED = "oversized", "Oversized"


class BottomLength(models.TextChoices):
    MICRO = "micro", "Micro"
    SHORT = "short", "Short"
    KNEE = "knee", "Knee"
    BELOW_KNEE = "below_knee", "Below Knee"
    CROPPED = "cropped", "Cropped"
    ANKLE = "ankle", "Ankle"
    FULL = "full", "Full"
    FLOOR = "floor", "Floor"


class StrapType(models.TextChoices):
    NONE = "none", "None"
    STRAPLESS = "strapless", "Strapless"
    SPAGHETTI = "spaghetti", "Spaghetti"
    THIN = "thin", "Thin"
    MEDIUM = "medium", "Medium"
    WIDE = "wide", "Wide"
    HALTER = "halter", "Halter"
    ONE_SHOULDER = "one_shoulder", "One Shoulder"


class Silhouette(models.TextChoices):
    STRAIGHT = "straight", "Straight"
    A_LINE = "a_line", "A-Line"
    BODYCON = "bodycon", "Bodycon"
    FIT_AND_FLARE = "fit_and_flare", "Fit and Flare"
    EMPIRE = "empire", "Empire"
    SHIFT = "shift", "Shift"
    SHEATH = "sheath", "Sheath"
    WRAP = "wrap", "Wrap"
    SLIP = "slip", "Slip"
    BALL_GOWN = "ball_gown", "Ball Gown"
    MERMAID = "mermaid", "Mermaid"


class DressLength(models.TextChoices):
    MINI = "mini", "Mini"
    ABOVE_KNEE = "above_knee", "Above Knee"
    KNEE = "knee", "Knee"
    MIDI = "midi", "Midi"
    MAXI = "maxi", "Maxi"
    FLOOR = "floor", "Floor"


class BackStyle(models.TextChoices):
    CLOSED = "closed", "Closed"
    OPEN_BACK = "open_back", "Open Back"
    LOW_BACK = "low_back", "Low Back"
    CROSS_BACK = "cross_back", "Cross Back"
    RACERBACK = "racerback", "Racerback"
    KEYHOLE = "keyhole", "Keyhole"
    LACE_UP = "lace_up", "Lace Up"


class LapelType(models.TextChoices):
    NONE = "none", "None"
    NOTCH = "notch", "Notch"
    PEAK = "peak", "Peak"
    SHAWL = "shawl", "Shawl"


class JacketLength(models.TextChoices):
    CROPPED = "cropped", "Cropped"
    WAIST = "waist", "Waist"
    HIP = "hip", "Hip"
    MID_THIGH = "mid_thigh", "Mid Thigh"
    KNEE = "knee", "Knee"
    BELOW_KNEE = "below_knee", "Below Knee"
    FULL_LENGTH = "full_length", "Full Length"


class Insulation(models.TextChoices):
    NONE = "none", "None"
    LIGHT = "light", "Light"
    MEDIUM = "medium", "Medium"
    HEAVY = "heavy", "Heavy"
    PADDED = "padded", "Padded"
    DOWN = "down", "Down"
    FLEECE_LINED = "fleece_lined", "Fleece Lined"


class ShoeHeight(models.TextChoices):
    LOW = "low", "Low"
    ANKLE = "ankle", "Ankle"
    MID = "mid", "Mid"
    HIGH = "high", "High"
    KNEE = "knee", "Knee"
    OVER_KNEE = "over_knee", "Over Knee"


class ToeShape(models.TextChoices):
    ROUND = "round", "Round"
    ALMOND = "almond", "Almond"
    SQUARE = "square", "Square"
    POINTED = "pointed", "Pointed"
    OPEN = "open", "Open"
    WIDE = "wide", "Wide"


class HeelType(models.TextChoices):
    NONE = "none", "None"
    FLAT = "flat", "Flat"
    BLOCK = "block", "Block"
    STILETTO = "stiletto", "Stiletto"
    KITTEN = "kitten", "Kitten"
    WEDGE = "wedge", "Wedge"
    PLATFORM = "platform", "Platform"
    CONE = "cone", "Cone"


class HeelHeight(models.TextChoices):
    NONE = "none", "None"
    FLAT = "flat", "Flat"
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    VERY_HIGH = "very_high", "Very High"


class ShoeClosure(models.TextChoices):
    NONE = "none", "None"
    SLIP_ON = "slip_on", "Slip On"
    LACES = "laces", "Laces"
    ZIPPER = "zipper", "Zipper"
    BUCKLE = "buckle", "Buckle"
    VELCRO = "velcro", "Velcro"
    STRAP = "strap", "Strap"
    ELASTIC = "elastic", "Elastic"


class SoleType(models.TextChoices):
    FLAT = "flat", "Flat"
    RUBBER = "rubber", "Rubber"
    FOAM = "foam", "Foam"
    LEATHER = "leather", "Leather"
    LUG = "lug", "Lug"
    PLATFORM = "platform", "Platform"
    CHUNKY = "chunky", "Chunky"
    CREPE = "crepe", "Crepe"


class ShoeProfile(models.TextChoices):
    MINIMAL = "minimal", "Minimal"
    STANDARD = "standard", "Standard"
    CHUNKY = "chunky", "Chunky"
    SLEEK = "sleek", "Sleek"
    ATHLETIC = "athletic", "Athletic"
    RUGGED = "rugged", "Rugged"


class WaistStyle(models.TextChoices):
    NONE = "none", "None"
    NATURAL = "natural", "Natural"
    HIGH = "high", "High"
    LOW = "low", "Low"
    ELASTIC = "elastic", "Elastic"
    DRAWSTRING = "drawstring", "Drawstring"
    BELTED = "belted", "Belted"
    FITTED = "fitted", "Fitted"


class ColorName(models.TextChoices):
    BLACK = "black", "Black"
    WHITE = "white", "White"
    GRAY = "gray", "Gray"
    CHARCOAL = "charcoal", "Charcoal"
    SILVER = "silver", "Silver"
    CREAM = "cream", "Cream"
    IVORY = "ivory", "Ivory"
    BEIGE = "beige", "Beige"
    TAN = "tan", "Tan"
    KHAKI = "khaki", "Khaki"
    CAMEL = "camel", "Camel"
    BROWN = "brown", "Brown"
    RED = "red", "Red"
    BURGUNDY = "burgundy", "Burgundy"
    MAROON = "maroon", "Maroon"
    PINK = "pink", "Pink"
    ROSE = "rose", "Rose"
    ORANGE = "orange", "Orange"
    CORAL = "coral", "Coral"
    PEACH = "peach", "Peach"
    YELLOW = "yellow", "Yellow"
    GOLD = "gold", "Gold"
    MUSTARD = "mustard", "Mustard"
    GREEN = "green", "Green"
    LIME = "lime", "Lime"
    OLIVE = "olive", "Olive"
    SAGE = "sage", "Sage"
    MINT = "mint", "Mint"
    EMERALD = "emerald", "Emerald"
    FOREST_GREEN = "forest_green", "Forest Green"
    BLUE = "blue", "Blue"
    NAVY = "navy", "Navy"
    ROYAL_BLUE = "royal_blue", "Royal Blue"
    SKY_BLUE = "sky_blue", "Sky Blue"
    BABY_BLUE = "baby_blue", "Baby Blue"
    TEAL = "teal", "Teal"
    TURQUOISE = "turquoise", "Turquoise"
    PURPLE = "purple", "Purple"
    LAVENDER = "lavender", "Lavender"
    VIOLET = "violet", "Violet"
    PLUM = "plum", "Plum"
    MULTICOLOR = "multicolor", "Multicolor"
    TRANSPARENT = "transparent", "Transparent"
    UNKNOWN = "unknown", "Unknown"


class ColorRole(models.TextChoices):
    PRIMARY = "primary", "Primary"
    SECONDARY = "secondary", "Secondary"
    ACCENT = "accent", "Accent"


class MaterialName(models.TextChoices):
    COTTON = "cotton", "Cotton"
    ORGANIC_COTTON = "organic_cotton", "Organic Cotton"
    DENIM = "denim", "Denim"
    LINEN = "linen", "Linen"
    WOOL = "wool", "Wool"
    MERINO_WOOL = "merino_wool", "Merino Wool"
    CASHMERE = "cashmere", "Cashmere"
    SILK = "silk", "Silk"
    SATIN = "satin", "Satin"
    VELVET = "velvet", "Velvet"
    CORDUROY = "corduroy", "Corduroy"
    LEATHER = "leather", "Leather"
    FAUX_LEATHER = "faux_leather", "Faux Leather"
    SUEDE = "suede", "Suede"
    FAUX_SUEDE = "faux_suede", "Faux Suede"
    POLYESTER = "polyester", "Polyester"
    NYLON = "nylon", "Nylon"
    ACRYLIC = "acrylic", "Acrylic"
    SPANDEX = "spandex", "Spandex"
    ELASTANE = "elastane", "Elastane"
    RAYON = "rayon", "Rayon"
    VISCOSE = "viscose", "Viscose"
    MODAL = "modal", "Modal"
    FLEECE = "fleece", "Fleece"
    JERSEY = "jersey", "Jersey"
    CANVAS = "canvas", "Canvas"
    MESH = "mesh", "Mesh"
    LACE = "lace", "Lace"
    CHIFFON = "chiffon", "Chiffon"
    TWEED = "tweed", "Tweed"
    RUBBER = "rubber", "Rubber"
    SYNTHETIC = "synthetic", "Synthetic"
    MIXED = "mixed", "Mixed"
    UNKNOWN = "unknown", "Unknown"


class PatternName(models.TextChoices):
    NONE = "none", "None"
    SOLID = "solid", "Solid"
    STRIPED = "striped", "Striped"
    CHECKED = "checked", "Checked"
    PLAID = "plaid", "Plaid"
    GINGHAM = "gingham", "Gingham"
    POLKA_DOT = "polka_dot", "Polka Dot"
    FLORAL = "floral", "Floral"
    ANIMAL_PRINT = "animal_print", "Animal Print"
    CAMOUFLAGE = "camouflage", "Camouflage"
    GEOMETRIC = "geometric", "Geometric"
    ABSTRACT = "abstract", "Abstract"
    PAISLEY = "paisley", "Paisley"
    TIE_DYE = "tie_dye", "Tie Dye"
    GRADIENT = "gradient", "Gradient"
    OMBRE = "ombre", "Ombre"
    COLOR_BLOCK = "color_block", "Color Block"
    GRAPHIC = "graphic", "Graphic"
    LOGO = "logo", "Logo"
    TEXT = "text", "Text"
    OTHER = "other", "Other"


class PatternScale(models.TextChoices):
    NONE = "none", "None"
    SMALL = "small", "Small"
    MEDIUM = "medium", "Medium"
    LARGE = "large", "Large"
    MIXED = "mixed", "Mixed"


class PatternDensity(models.TextChoices):
    NONE = "none", "None"
    SPARSE = "sparse", "Sparse"
    MEDIUM = "medium", "Medium"
    DENSE = "dense", "Dense"


class PatternOrientation(models.TextChoices):
    NONE = "none", "None"
    HORIZONTAL = "horizontal", "Horizontal"
    VERTICAL = "vertical", "Vertical"
    DIAGONAL = "diagonal", "Diagonal"
    MIXED = "mixed", "Mixed"


class DetailName(models.TextChoices):
    EMBROIDERY = "embroidery", "Embroidery"
    SEQUINS = "sequins", "Sequins"
    BEADING = "beading", "Beading"
    RHINESTONES = "rhinestones", "Rhinestones"
    STUDS = "studs", "Studs"
    FRINGE = "fringe", "Fringe"
    TASSELS = "tassels", "Tassels"
    RUFFLES = "ruffles", "Ruffles"
    BOWS = "bows", "Bows"
    LACE = "lace", "Lace"
    PATCHES = "patches", "Patches"
    APPLIQUE = "applique", "Applique"
    DISTRESSING = "distressing", "Distressing"
    RIPS = "rips", "Rips"
    CUTOUTS = "cutouts", "Cutouts"
    PLEATS = "pleats", "Pleats"
    GATHERS = "gathers", "Gathers"
    SMOCKING = "smocking", "Smocking"
    QUILTING = "quilting", "Quilting"
    CONTRAST_STITCHING = "contrast_stitching", "Contrast Stitching"
    PIPING = "piping", "Piping"
    CHAINS = "chains", "Chains"
    BUCKLES = "buckles", "Buckles"
    VISIBLE_BUTTONS = "visible_buttons", "Visible Buttons"
    VISIBLE_ZIPPERS = "visible_zippers", "Visible Zippers"
    LOGO = "logo", "Logo"
    GRAPHIC = "graphic", "Graphic"
    TEXT = "text", "Text"


class StyleName(models.TextChoices):
    MINIMALIST = "minimalist", "Minimalist"
    CLASSIC = "classic", "Classic"
    CASUAL = "casual", "Casual"
    SMART_CASUAL = "smart_casual", "Smart Casual"
    BUSINESS_CASUAL = "business_casual", "Business Casual"
    FORMAL = "formal", "Formal"
    PREPPY = "preppy", "Preppy"
    OLD_MONEY = "old_money", "Old Money"
    QUIET_LUXURY = "quiet_luxury", "Quiet Luxury"
    STREETWEAR = "streetwear", "Streetwear"
    URBAN = "urban", "Urban"
    SKATER = "skater", "Skater"
    SPORTY = "sporty", "Sporty"
    ATHLEISURE = "athleisure", "Athleisure"
    WORKWEAR = "workwear", "Workwear"
    UTILITY = "utility", "Utility"
    MILITARY = "military", "Military"
    OUTDOORSY = "outdoorsy", "Outdoorsy"
    GORPCORE = "gorpcore", "Gorpcore"
    TECHWEAR = "techwear", "Techwear"
    VINTAGE = "vintage", "Vintage"
    RETRO = "retro", "Retro"
    Y2K = "y2k", "Y2K"
    BOHEMIAN = "bohemian", "Bohemian"
    ROMANTIC = "romantic", "Romantic"
    WESTERN = "western", "Western"
    GRUNGE = "grunge", "Grunge"
    PUNK = "punk", "Punk"
    GOTHIC = "gothic", "Gothic"
    EDGY = "edgy", "Edgy"
    AVANT_GARDE = "avant_garde", "Avant Garde"


class PocketTypeName(models.TextChoices):
    SIDE = "side", "Side"
    SLASH = "slash", "Slash"
    PATCH = "patch", "Patch"
    CHEST = "chest", "Chest"
    CARGO = "cargo", "Cargo"
    WELT = "welt", "Welt"
    ZIPPERED = "zippered", "Zippered"
    KANGAROO = "kangaroo", "Kangaroo"
    BACK = "back", "Back"
    COIN = "coin", "Coin"
    HIDDEN = "hidden", "Hidden"
    FLAP = "flap", "Flap"


class Brightness(models.TextChoices):
    VERY_DARK = "very_dark", "Very Dark"
    DARK = "dark", "Dark"
    MEDIUM = "medium", "Medium"
    LIGHT = "light", "Light"
    VERY_LIGHT = "very_light", "Very Light"


class Saturation(models.TextChoices):
    DESATURATED = "desaturated", "Desaturated"
    MUTED = "muted", "Muted"
    MEDIUM = "medium", "Medium"
    VIBRANT = "vibrant", "Vibrant"
    HIGHLY_VIBRANT = "highly_vibrant", "Highly Vibrant"


class VisualComplexity(models.TextChoices):
    VERY_SIMPLE = "very_simple", "Very Simple"
    SIMPLE = "simple", "Simple"
    MODERATE = "moderate", "Moderate"
    BUSY = "busy", "Busy"
    VERY_BUSY = "very_busy", "Very Busy"


class StatementLevel(models.TextChoices):
    BASIC = "basic", "Basic"
    SUBTLE = "subtle", "Subtle"
    MODERATE = "moderate", "Moderate"
    STATEMENT = "statement", "Statement"
    BOLD = "bold", "Bold"


class Structure(models.TextChoices):
    SOFT = "soft", "Soft"
    SEMI_STRUCTURED = "semi_structured", "Semi Structured"
    STRUCTURED = "structured", "Structured"
    RIGID = "rigid", "Rigid"


class SurfaceFinish(models.TextChoices):
    MATTE = "matte", "Matte"
    SEMI_MATTE = "semi_matte", "Semi Matte"
    SEMI_GLOSS = "semi_gloss", "Semi Gloss"
    GLOSSY = "glossy", "Glossy"
    METALLIC = "metallic", "Metallic"
    SPARKLY = "sparkly", "Sparkly"


class Transparency(models.TextChoices):
    OPAQUE = "opaque", "Opaque"
    SLIGHTLY_SHEER = "slightly_sheer", "Slightly Sheer"
    SHEER = "sheer", "Sheer"
    TRANSPARENT = "transparent", "Transparent"


class Symmetry(models.TextChoices):
    SYMMETRIC = "symmetric", "Symmetric"
    MOSTLY_SYMMETRIC = "mostly_symmetric", "Mostly Symmetric"
    ASYMMETRIC = "asymmetric", "Asymmetric"
