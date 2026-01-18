# TTCP Tracking System - Setup & Admin Guide

## ✅ System Overview

The tracking system is now **fully integrated** with Django backend:

- **Admin Interface**: Create/edit shipments and tracking events at `/admin/`
- **API Endpoints**: Return shipment data as JSON
- **Frontend**: Automatically fetches and displays real data from backend

---

## 🚀 Quick Start

### 1. Database Setup (Run Once)

```bash
# Create new database tables for Shipment and ShipmentEvent models
python manage.py makemigrations tracking
python manage.py migrate
```

### 2. Create Admin User (If Not Exists)

```bash
python manage.py createsuperuser
```

Then visit: **`http://localhost:8000/admin/`**

Login with your admin credentials.

---

## 📋 Admin Workflow

### Creating a Shipment in Admin

1. Go to **Shipments** section in Django Admin
2. Click **"Add Shipment"** 
3. Fill in the following organized sections:

#### **Tracking Info** (Required)
- **Tracking Number**: Unique identifier (e.g., `TTCP123456789`)
- **Status**: Choose one of:
  - `created` - Initial status (25% progress)
  - `in_transit` - In transit (50% progress)
  - `out_for_delivery` - Out for delivery (75% progress)
  - `delivered` - Delivered (100% progress)
  - `failed` - Delivery failed

#### **Sender Information** (Optional)
- Sender Name (default: "Smith Industries")
- Sender Email
- Sender Phone

#### **Receiver Information** (Optional)
- Receiver Name (default: "Johnson & Co.")
- Receiver Email
- Receiver Phone

#### **Package Information** (Optional)
- Package Description (default: "Electronic Components & Parts")
- Weight (in kg)
- Dimensions

#### **Origin Location** (Optional)
- Origin City (e.g., "New York, USA")
- Origin Latitude
- Origin Longitude

#### **Destination Location** (Optional)
- Destination City (e.g., "Los Angeles, USA")
- Destination Latitude
- Destination Longitude

#### **Current Status** (Optional)
- Current Location (displayed on tracking page)
- Current Latitude (map marker position)
- Current Longitude (map marker position)

#### **Delivery** (Optional)
- Estimated Delivery Date/Time

4. Click **Save**

### Adding Tracking Events

1. Go to **Shipment Events** section in Django Admin
2. Click **"Add Shipment Event"**
3. Fill in:
   - **Shipment**: Select the shipment to track
   - **Status**: Event title (e.g., "Package Picked Up")
   - **Location**: Where the event occurred
   - **Latitude/Longitude**: Event coordinates (optional)
   - **Notes**: Event description
   - **Timestamp**: When event occurred (auto-filled with current time)

4. Click **Save**

**Repeat for each tracking milestone** (Picked up, In Transit, Out for Delivery, Delivered, etc.)

---

## 🗺️ Data Flow Diagram

```
Admin Interface (/admin/)
    ↓
    ├→ Create Shipment Record
    │   └→ All fields stored in database
    ├→ Create ShipmentEvent Records (1 to many)
    │   └→ Tracking timeline events
    ↓
Database (SQLite/PostgreSQL)
    ↓
API Endpoint (/api/shipment/{tracking_number}/)
    ├→ Returns complete Shipment object
    ├→ Includes: sender, receiver, package, progress, events
    └→ JSON format ready for frontend
    ↓
Frontend (track.html)
    ├→ JavaScript calls: fetchTrackingData()
    ├→ Receives JSON from API
    ├→ Displays: info, timeline, map
    └→ Map shows: current_lat, current_lng
```

---

## 🔗 API Endpoints

### 1. **Get Shipment Details** (Full)
```
GET /api/shipment/{tracking_number}/
```

**Example Request:**
```
http://localhost:8000/api/shipment/TTCP123456789/
```

**Response:**
```json
{
    "tracking_number": "TTCP123456789",
    "status": "in_transit",
    "progress": 50,
    "origin": "New York, USA",
    "destination": "Los Angeles, USA",
    "weight": 15.5,
    "sender_name": "Smith Industries",
    "receiver_name": "Johnson & Co.",
    "receiver_phone": "+1 (555) 123-4567",
    "package_description": "Electronic Components",
    "est_delivery": "01/22/2026",
    "current_lat": 40.7128,
    "current_lng": -74.0060,
    "current_location": "Distribution Center, NY",
    "created_at": "01/18/2026 10:30",
    "events": [
        {
            "status": "Shipment Created",
            "location": "New York, USA",
            "timestamp": "01/18/2026 10:30",
            "description": "Package received and processed"
        },
        {
            "status": "In Transit",
            "location": "Distribution Center",
            "timestamp": "01/20/2026 15:45",
            "description": "Package in transit to destination"
        }
    ]
}
```

### 2. **Get Location Only** (Quick)
```
GET /api/shipment/{tracking_number}/location/
```

**Response:**
```json
{
    "tracking_number": "TTCP123456789",
    "current_lat": 40.7128,
    "current_lng": -74.0060,
    "status": "in_transit",
    "progress": 50.0
}
```

### 3. **List All Shipments** (Paginated)
```
GET /api/shipments/?page=1&limit=20
```

**Response:**
```json
{
    "total": 5,
    "page": 1,
    "limit": 20,
    "shipments": [
        {
            "tracking_number": "TTCP123456789",
            "status": "in_transit",
            "origin": "New York, USA",
            "destination": "Los Angeles, USA",
            "created_at": "2026-01-18 10:30"
        }
    ]
}
```

---

## 🧪 Testing the System

### Test 1: Check API Endpoint
```
1. Open browser: http://localhost:8000/api/shipment/TTCP123456789/
2. Should see JSON response
3. All fields should match admin data
```

### Test 2: Track a Package
```
1. Visit: http://localhost:8000/track/?q=TTCP123456789
2. Or: http://localhost:8000/track/?tracking=TTCP123456789
3. Page should display:
   - Tracking number
   - Status badge (with icon)
   - Progress bar
   - All shipment details
   - Timeline with all events
   - Map with current location
```

### Test 3: Manual Search
```
1. Visit: http://localhost:8000/track/
2. Enter tracking number in search box
3. Click "Track" button or press Enter
4. Should display all tracking info
```

---

## 📝 Sample Data Creation

Create a test shipment:

**In Django Admin:**
1. Go to Shipments → Add Shipment
2. Tracking Number: `TEST001`
3. Sender Name: `Test Sender`
4. Receiver Name: `Test Receiver`
5. Origin: `New York, USA`
6. Current Latitude: `40.7128`
7. Current Longitude: `-74.0060`
8. Status: `in_transit`
9. Save

Then add events:
1. Go to Shipment Events → Add Event
2. Shipment: Select `TEST001`
3. Status: `Package Picked Up`
4. Location: `New York Hub`
5. Notes: `Initial pickup from sender`
6. Save

Visit tracking page:
```
http://localhost:8000/track/?q=TEST001
```

---

## 🐛 Troubleshooting

### Problem: "Tracking number not found"
**Solution**: 
1. Check if shipment exists in admin
2. Verify tracking number matches exactly (case-sensitive)
3. Check API directly: `/api/shipment/{number}/`

### Problem: Map not showing
**Solution**:
1. Verify `current_lat` and `current_lng` are set
2. Check browser console for JavaScript errors
3. Leaflet library loads from CDN (requires internet)

### Problem: Events not displaying
**Solution**:
1. Go to admin → Shipment Events
2. Verify events are linked to correct shipment
3. Check that event details are filled in

### Problem: 404 error on API call
**Solution**:
1. Verify migrations ran: `python manage.py migrate`
2. Check Shipment model fields exist
3. Verify tracking number in database

---

## 🔐 Security Notes

- Admin interface is at `/admin/` - **only authorized staff can access**
- API endpoints are **public read-only** (no authentication required)
- All shipment data is **manually entered by admins**
- Status is auto-calculated from selected status field

---

## 📱 Field Reference

### Shipment Model Fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `tracking_number` | String | ✅ Yes | Unique identifier |
| `status` | Choice | ✅ Yes | Auto-calculates progress |
| `sender_name` | String | ❌ | Default: "Smith Industries" |
| `sender_email` | Email | ❌ | Optional |
| `sender_phone` | String | ❌ | Optional |
| `receiver_name` | String | ❌ | Default: "Johnson & Co." |
| `receiver_email` | Email | ❌ | Optional |
| `receiver_phone` | String | ❌ | Optional |
| `package_description` | String | ❌ | Default: "Electronic Components & Parts" |
| `weight` | Float | ❌ | In kg |
| `dimensions` | String | ❌ | Optional |
| `origin` | String | ❌ | City/location |
| `destination` | String | ❌ | City/location |
| `origin_lat` | Float | ❌ | For map |
| `origin_lng` | Float | ❌ | For map |
| `dest_lat` | Float | ❌ | For map |
| `dest_lng` | Float | ❌ | For map |
| `current_lat` | Float | ❌ | Map marker position |
| `current_lng` | Float | ❌ | Map marker position |
| `current_location` | String | ❌ | Display text |
| `estimated_delivery` | DateTime | ❌ | Delivery date |

### ShipmentEvent Model Fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `shipment` | ForeignKey | ✅ Yes | Link to Shipment |
| `status` | String | ✅ Yes | Event title |
| `location` | String | ❌ | Where event occurred |
| `notes` | Text | ❌ | Event description |
| `latitude` | Float | ❌ | Event coordinates |
| `longitude` | Float | ❌ | Event coordinates |
| `timestamp` | DateTime | ✅ Auto | Auto-filled, can be modified |

---

## 🎯 Progress Calculation

Progress automatically calculated from `status`:
- `created` → 25%
- `in_transit` → 50%
- `out_for_delivery` → 75%
- `delivered` → 100%

**No manual entry needed!**

---

## 📞 Support

For API issues, check:
1. Django server is running: `python manage.py runserver`
2. Migrations are applied: `python manage.py migrate`
3. Admin user created: `python manage.py createsuperuser`
4. Shipment data exists in admin

---

**System Ready!** 🎉 Enter your shipment data in admin and watch it display on the tracking page!
