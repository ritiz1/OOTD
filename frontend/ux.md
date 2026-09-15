# Wardrobe Outfit Planner — UX Specification

## 1. Product Goal

The app helps a user:

1. Log individual clothing items into a personal wardrobe by uploading photos.
2. Enter the schedule for a day.
3. Automatically consider weather for each scheduled event.
4. Generate one outfit plan for the entire day.
5. Intelligently decide whether the user should keep the same outfit or change specific clothing items between events.

The experience should feel minimal, fast, and Apple-like.

---

## 2. Main Navigation

Bottom navigation:

- **Home**
- **Wardrobe**
- **Plan**
- **Profile**

### Home
Shows today's schedule and today's generated outfit plan.

### Wardrobe
Shows and manages all saved clothing items.

### Plan
Used to create a plan for a future day.

### Profile
Basic account and app settings.

---

# 3. First-Time User Experience

After registration/login, the user lands on **Home / Plan My Day**.

If the wardrobe is empty:

- Show a clear empty state.
- Explain that clothing needs to be added before useful outfit suggestions can be generated.
- Do not hard-block the rest of the app.
- Primary CTA: **Add Clothes**
- Secondary CTA: **Plan My Day**

Example empty state:

> Your wardrobe is empty.  
> Add a few clothing items so we can build outfits from clothes you actually own.

Button:

**Add Clothes**

---

# 4. Home — Plan My Day

Home is focused on **today**.

## Empty / Not Planned State

Header:

**Plan My Day**

Show today's date.

Main content:

- Today's schedule
- Button to add events
- Generate Outfit button

If there are no events:

> What are you doing today?

Primary CTA:

**+ Add Event**

---

# 5. Adding Schedule Events

Schedule entry uses a structured timeline form.

The user does **not** manually enter weather.

## Add Event Form

Fields:

- Activity
- Start Time
- End Time

Example:

**Activity**  
Class on campus

**Start Time**  
9:00 AM

**End Time**  
11:00 AM

Button:

**Add Event**

After adding an event, it appears in the day's timeline.

Example:

### 9:00 AM – 11:00 AM
Class on campus

### 7:00 PM – 9:00 PM
Casual dinner indoors

Users can:

- Add event
- Edit event
- Delete event

Events are automatically ordered by start time.

---

# 6. Weather Enrichment

After events are added, the app automatically attaches weather data based on:

- User location
- Event time
- Forecast

The user does not manually enter weather.

Backend representation may look like:

```json
{
  "schedule": [
    {
      "event_id": "morning-class",
      "start_time": "09:00",
      "end_time": "11:00",
      "activity": "Class on campus",
      "weather": {
        "status": "cool and breezy",
        "temperature_c": 12,
        "precipitation": "none"
      }
    },
    {
      "event_id": "evening-dinner",
      "start_time": "19:00",
      "end_time": "21:00",
      "activity": "Casual dinner indoors",
      "weather": {
        "status": "mild and dry",
        "temperature_c": 19,
        "precipitation": "none"
      }
    }
  ]
}
```

In the UI, weather should remain compact.

Example:

**9:00 AM – 11:00 AM**  
Class on campus  
12°C · Cool & breezy

---

# 7. Generate Outfit

Once at least one event exists, show the primary action:

**Generate Outfit**

The system creates **one recommendation for the whole day**.

The recommendation engine should determine:

- Which clothing items work for the first event.
- Whether the same outfit can continue into later events.
- Whether specific items should be added, removed, or replaced.
- Whether a full outfit change is necessary.

---

# 8. Outfit Recommendation Screen

The recommendation is displayed as a **timeline + individual clothing cards**.

Example:

## Your Outfit Today

### 9:00 AM – 11:00 AM
**Class on campus**

12°C · Cool & breezy

Clothing cards:

- Jacket
- T-Shirt
- Jeans
- Sneakers

Each card contains:

- Clothing photo
- Clothing type/name

---

### 11:00 AM – 7:00 PM

**Keep the same outfit**

If conditions change, the app may show:

**Remove Jacket**

---

### 7:00 PM – 9:00 PM
**Casual dinner indoors**

19°C · Mild & dry

**Change:**

Jacket → Overshirt

**Keep:**

- T-Shirt
- Jeans
- Sneakers

The goal is to clearly communicate:

- what the user should wear,
- what stays the same,
- what changes,
- and when it changes.

---

# 9. Regenerate

There is one regenerate action for the complete day.

Button:

**Regenerate Outfit**

Pressing it generates a completely new daily outfit recommendation.

There is no event-level regenerate in V1.

---

# 10. Wardrobe

The Wardrobe screen contains the user's individual clothing items.

## Layout

Use a photo-first grid.

Top area:

**Wardrobe**

Controls:

- Search
- Filter
- Add Clothing

Category selector:

- All
- Tops
- Bottoms
- Outerwear
- Shoes
- Other

Below:

Responsive clothing photo grid.

Each grid item primarily displays the clothing image.

Optional small secondary text:

- T-Shirt
- Jeans
- Sneakers

The visual design should remain image-first.

---

# 11. Add Clothing

Primary action:

**+ Add Clothing**

V1 input method:

**Upload Photo**

The uploaded image should contain one individual clothing item, not a complete outfit.

## Upload Flow

1. User selects a photo.
2. Upload begins.
3. AI analyzes the clothing.
4. Clothing item is automatically saved.
5. User receives confirmation.

Example:

**Added to Wardrobe**

Secondary action:

**Edit Details**

The user is not forced through an attribute-editing form during upload.

This keeps wardrobe logging fast.

---

# 12. Clothing AI Analysis

The system automatically extracts visual clothing attributes such as:

- Type
- Color
- Material
- Pattern
- Style
- Other supported visual attributes

The AI-generated values are stored with the clothing item.

Users can edit them later.

---

# 13. Clothing Detail Screen

When a wardrobe item is tapped, open its detail screen.

Show:

- Large clothing image
- Clothing type
- Detected attributes

Actions:

- **Edit**
- **Delete**

## Edit

Allows the user to modify detected clothing attributes.

## Delete

Show confirmation before deletion.

Example:

> Remove this item from your wardrobe?

Buttons:

- Cancel
- Delete

---

# 14. Search and Filters

Wardrobe supports:

## Search

Search clothing by detected information such as:

- Type
- Color
- Material
- Style

Example:

`black jacket`

## Filters

At minimum:

- Category
- Color
- Type

Filters should open in a compact bottom sheet rather than a large separate screen.

---

# 15. Plan Tab

The **Plan** tab is for a future day.

Example:

**Plan a Day**

Date selector:

`September 18`

Then the same schedule builder used on Home:

- Add Event
- Edit Event
- Delete Event
- Generate Outfit

Home is specifically for **today**.

Plan is for **future dates**.

---

# 16. Profile

V1 Profile should remain simple.

Sections:

## Account
- Name
- Email

## Settings
- Units
- Location permission
- Notifications
- Appearance

## Account Actions
- Log Out

Do not add advanced fashion preference configuration in V1.

---

# 17. Important UX States

## Empty Wardrobe

Show:

> Add clothes to get outfit recommendations from your own wardrobe.

CTA:

**Add Clothes**

---

## Wardrobe Has Too Few Items

The user can still generate recommendations when possible.

If a complete outfit cannot be created:

> We couldn't build a complete outfit from your current wardrobe.

CTA:

**Add More Clothes**

---

## No Schedule

Show:

> Add your plans for today and we'll build an outfit around them.

CTA:

**Add Event**

---

## Generating

Show a lightweight loading state.

Example:

**Building your outfit…**

Avoid excessive animation or conversational text.

---

## Generation Failed

Show:

> Couldn't generate an outfit right now.

Buttons:

- Try Again
- Edit Schedule

---

## Weather Unavailable

Do not block planning.

Show:

**Weather unavailable**

Generate the recommendation using activity information and available wardrobe data.

---

# 18. Primary User Flow

```text
LOGIN
  ↓
HOME — PLAN MY DAY
  ↓
ADD SCHEDULE EVENTS
  ↓
APP FETCHES WEATHER
  ↓
GENERATE OUTFIT
  ↓
DAILY OUTFIT TIMELINE
  ↓
WEAR SAME OUTFIT
        OR
CHANGE SPECIFIC ITEMS BETWEEN EVENTS
```

---

# 19. Wardrobe Creation Flow

```text
WARDROBE
   ↓
+ ADD CLOTHING
   ↓
UPLOAD PHOTO
   ↓
AI ANALYZES ITEM
   ↓
AUTO-SAVE
   ↓
ITEM APPEARS IN WARDROBE GRID
   ↓
OPTIONAL: OPEN ITEM → EDIT DETAILS
```

---

# 20. Screen Structure

```text
APP
│
├── HOME
│   ├── Today's Schedule
│   ├── Add Event
│   ├── Weather
│   ├── Generate Outfit
│   └── Today's Outfit Timeline
│
├── WARDROBE
│   ├── Search
│   ├── Filters
│   ├── Categories
│   ├── Clothing Grid
│   ├── Add Clothing
│   │    └── Upload Photo
│   └── Clothing Detail
│        ├── View Attributes
│        ├── Edit
│        └── Delete
│
├── PLAN
│   ├── Date Selector
│   ├── Schedule Timeline
│   ├── Add Event
│   ├── Weather
│   └── Generate Outfit
│
└── PROFILE
    ├── Account
    ├── Settings
    └── Log Out
```

---

# 21. Visual Direction

Overall style:

**Minimal / Apple-like**

Principles:

- Large amounts of whitespace
- Large clothing photography
- Minimal text
- Clear visual hierarchy
- Rounded cards
- Simple iconography
- Avoid excessive borders
- Avoid dense dashboards
- One obvious primary action per screen
- Use bottom sheets for lightweight editing/filtering
- Smooth transitions between schedule and outfit timeline
- Clothing imagery should remain the strongest visual element

The app should feel like a personal utility, not a social network or fashion marketplace.
