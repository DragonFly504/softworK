# TTCP Tracking System - Quick Admin Reference

## 🚀 Start Here

### First Time Setup (One-time only)
```bash
python manage.py makemigrations tracking
python manage.py migrate
python manage.py createsuperuser
```

### Run Django Server
```bash
python manage.py runserver
```

Then go to: **`http://localhost:8000/admin/`**

---

## 📋 Typical Workflow

### 1️⃣ Create New Shipment
- Go to **Shipments** section
- Click **Add Shipment**
- **REQUIRED**: Enter unique tracking number
- Fill in sender/receiver/package info (optional)
- Set **Status** (auto-calculates progress)
- Save

### 2️⃣ Add Tracking Events (Timeline)
- Go to **Shipment Events** section
- Click **Add Event** for each milestone
- Select the **Shipment** 
- Enter **Status** (what happened)
- Enter **Location** (where it happened)
- Add **Notes** (description)
- Save

### 3️⃣ Track on Website
- Visit: `http://localhost:8000/track/?q=TRACKINGNUMBER`
- Or use search box on tracking page

---

## ⚡ Quick Actions

### View All Shipments
- **Dashboard**: Shipments list in Admin
- **Search**: Use search bar to find by tracking number, sender, receiver

### View All Events
- **Dashboard**: Shipment Events list in Admin
- **Filter**: By status or date

### Test a Tracking Number
- Visit: `http://localhost:8000/api/shipment/YOURTRACKING/`
- Should return JSON with all shipment data

---

## 📊 Status Options & Progress

When creating/editing a shipment, choose status:

| Status | Progress | Icon | Meaning |
|--------|----------|------|---------|
| `created` | 25% | ✓ | Package ready/created |
| `in_transit` | 50% | 📦 | Moving to destination |
| `out_for_delivery` | 75% | 🚚 | Out with driver |
| `delivered` | 100% | ✓ | Delivered to recipient |
| `failed` | - | ❌ | Delivery issue |

**Progress auto-calculates!** No manual entry needed.

---

## 🗺️ Map Coordinates

For map to work on tracking page:

**In Shipment record:**
- Set `current_lat` and `current_lng` (current location marker)
- Optional: `origin_lat`, `origin_lng`, `dest_lat`, `dest_lng`

**In Events (optional):**
- Set `latitude` and `longitude` for event location markers

**Default location**: New York (40.7128, -74.0060) if not specified

---

## 🔗 URL Shortcuts

| Page | URL |
|------|-----|
| Admin Dashboard | `/admin/` |
| Add Shipment | `/admin/tracking/shipment/add/` |
| All Shipments | `/admin/tracking/shipment/` |
| Add Event | `/admin/tracking/shipmentevent/add/` |
| All Events | `/admin/tracking/shipmentevent/` |
| Public Track Page | `/track/` |
| Track Specific | `/track/?q=TRACKINGNUMBER` |

---

## 📝 Common Data Fields

### Shipment Minimum Required
- ✅ **Tracking Number** (unique ID)

### Shipment Recommended (for complete info)
- Sender Name
- Receiver Name
- Receiver Phone
- Package Description
- Origin
- Destination
- Current Location
- Current Lat/Lng (for map)
- Estimated Delivery
- Status

### Event Minimum Required
- ✅ **Shipment** (which package)
- ✅ **Status** (what happened)

### Event Recommended
- Location (where)
- Notes (details)
- Timestamp (when - auto-filled)

---

## ❓ FAQ

**Q: Do I need to set all fields?**
A: No! Only tracking number is required. Fill what you have.

**Q: How does progress calculate?**
A: Automatically from status field. E.g., in_transit = 50%.

**Q: How many events per shipment?**
A: As many as you want (unlimited).

**Q: Can I edit after saving?**
A: Yes! Click shipment/event to edit anytime.

**Q: Can customers create shipments?**
A: No. Only admins via `/admin/`. Public only sees tracking.

**Q: What if coordinates are wrong?**
A: Map will show default (New York) or your coordinates.

---

## 🧪 Test It

```bash
# 1. Create Shipment with tracking number: TEST001
# 2. Add event: "Picked Up at New York"
# 3. Visit: http://localhost:8000/track/?q=TEST001
# 4. Should show all info + map + timeline
```

---

## 🆘 If Something Breaks

### API returns 404
```
→ Tracking number doesn't exist in database
→ Check Admin > Shipments for the tracking number
```

### Map not showing
```
→ Make sure current_lat and current_lng are set
→ Check browser console for JavaScript errors
```

### Timeline empty
```
→ Add events in Admin > Shipment Events
→ Make sure events are linked to correct shipment
```

### Page shows "Tracking number not found"
```
→ Verify tracking number in URL matches exactly in database
→ Tracking numbers are case-sensitive
```

---

## 💾 Backup Your Data

Your data is in SQLite database (db.sqlite3). To backup:
```bash
# Copy this file to safe location:
cp db.sqlite3 db.sqlite3.backup
```

---

**Everything Configured!** Start entering shipments in admin and track them on the website. 🚀
