# Clothing Model Skeleton

**Stable V1 structure to mirror across PostgreSQL, FastAPI, and Kotlin.**

---

## 1. Core Relationship Model

```text
USER
 |
 | 1:N
 v
CLOTHING_ITEM
 |-- 1:N --> CLOTHING_IMAGE
 `-- 1:1 --> CLOTHING_VISUAL_PROFILE
                 |
                 `--> attributes (extensible visual data)
```

---

## 2. Database Models

### USER

```text
id
name
email
```

### CLOTHING_ITEM

```text
id
user_id
category
subcategory
created_at
updated_at
```

### CLOTHING_IMAGE

```text
id
clothing_id
image_url
is_primary
created_at
```

### CLOTHING_VISUAL_PROFILE

```text
clothing_id
schema_version
attributes
analysis_model
analysis_model_version
created_at
updated_at
```

---

## 3. Shared App Models

### ClothingItem

```text
ClothingItem
|- id
|- userId
|- category
|- subcategory
|- images[]
|- visualProfile
|- createdAt
`- updatedAt
```

### ClothingImage

```text
ClothingImage
|- id
|- imageUrl
`- isPrimary
```

### ClothingVisualProfile

```text
ClothingVisualProfile
|- schemaVersion
`- attributes
```

---

## 4. Visual Attributes

```text
attributes
|-- colors
|   |-- primary
|   |-- secondary[]
|   `-- accent[]
|
|-- pattern
|   |-- type
|   `-- scale
|
|-- fabric
|   |-- materials[]
|   |-- texture
|   |-- finish
|   `-- weight
|
|-- shape
|   |-- fit
|   |-- silhouette
|   `-- length
|
|-- construction
|   |-- closure
|   `-- pockets[]
|
|-- details[]
|-- style_tags[]
`-- category_attributes
```

---

## 5. Category-Specific Attributes

### TOP

```text
sleeve_length
sleeve_type
neckline
collar
hood
hem
```

### BOTTOM

```text
rise
leg_shape
waistband
hem
```

### DRESS

```text
sleeve_length
neckline
strap_type
dress_length
back_style
```

### OUTERWEAR

```text
sleeve_length
collar
lapel
hood
jacket_length
```

### FOOTWEAR

```text
shoe_height
toe_shape
heel_type
heel_height
closure
sole_type
```

---

## 6. Mirror This Skeleton Everywhere

### DATABASE

```text
ClothingItem
ClothingImage
ClothingVisualProfile
```

### FASTAPI

```text
ClothingItem
ClothingImage
ClothingVisualProfile
    `- attributes = flexible object
```

### KOTLIN

```text
ClothingItem
ClothingImage
ClothingVisualProfile
    `- attributes = flexible JSON object
```

---

## 7. Stability Rule

### Keep Stable

```text
ClothingItem
ClothingImage
ClothingVisualProfile
```

### Expand

```text
visualProfile.attributes
category_attributes
```

New visual features should normally be added inside `attributes` so older Kotlin clients and the main database relationship remain stable.
