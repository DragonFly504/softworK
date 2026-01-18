# 🚚 TTCP Worldwide Tracking System

> A complete, production-ready shipment tracking system with Django backend admin and interactive frontend.

---

## ✨ Features

### 🎯 For Admins
- **Easy Data Entry**: Organized Django admin interface with logical fieldsets
- **Complete Control**: Manually enter all shipment and tracking information
- **Event Management**: Create unlimited tracking events for each shipment
- **Search & Filter**: Quickly find shipments by tracking number, sender, receiver, location
- **Real-time Updates**: Changes instantly visible to customers

### 🗺️ For Customers
- **Track Packages**: Search by tracking number
- **Real-time Info**: Current location and status
- **Timeline View**: Complete history of tracking events
- **Interactive Map**: Visual representation of current location
- **Responsive Design**: Works on desktop and mobile

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Django 4.0+
- SQLite (included with Python)

### Installation

```bash
# 1. Navigate to project directory
cd c:\Users\USER\Desktop\TTT-PROJECT

# 2. Install dependencies (if needed)
pip install -r requirements.txt

# 3. Run migrations
python manage.py makemigrations tracking
python manage.py migrate

# 4. Create admin user
python manage.py createsuperuser

# 5. Start development server
python manage.py runserver
```

### Access Points

| URL | Purpose |
|-----|---------|
| `http://localhost:8000/` | Homepage |
| `http://localhost:8000/track/` | Public tracking page |
| `http://localhost:8000/admin/` | Admin interface (staff only) |
| `http://localhost:8000/api/shipment/{number}/` | API endpoint |

---

## 📋 Admin Workflow

### 1. Create a Shipment
```
Admin Dashboard → Shipments → Add Shipment
├─ Tracking Number: TTCP123456789 (required)
├─ Sender Info: Name, Email, Phone
├─ Receiver Info: Name, Email, Phone
├─ Package: Description, Weight, Dimensions
├─ Locations: Origin, Destination, Current (with coordinates)
├─ Status: created | in_transit | out_for_delivery | delivered | failed
└─ Save
```

### 2. Add Tracking Events
```
Admin Dashboard → Shipment Events → Add Event
├─ Shipment: Select the shipment to track
├─ Status: Event title (e.g., "Picked Up")
├─ Location: Where event occurred
├─ Notes: Event description
└─ Save (repeat for each milestone)
```

### 3. Track on Website
```
Visit: http://localhost:8000/track/?q=TTCP123456789
```

All information displays automatically!

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────┐
│            PUBLIC TRACKING PAGE              │
│         (track.html - No Sample Data)        │
└────────────────┬────────────────────────────┘
                 │
                 │ fetch() calls
                 ↓
┌─────────────────────────────────────────────┐
│          DJANGO REST API ENDPOINTS           │
│  /api/shipment/{tracking_number}/           │
│  /api/shipment/{tracking_number}/location/  │
│  /api/shipments/                            │
└────────────────┬────────────────────────────┘
                 │
                 │ ORM queries
                 ↓
┌─────────────────────────────────────────────┐
│        DJANGO MODELS & ADMIN INTERFACE      │
│  Shipment | ShipmentEvent                   │
│  (to_dict() serialization methods)          │
└────────────────┬────────────────────────────┘
                 │
                 │ Database operations
                 ↓
┌─────────────────────────────────────────────┐
│           SQLITE DATABASE                    │
│  tracking_shipment | tracking_shipmentevent │
└─────────────────────────────────────────────┘
```

---

## 📊 Data Models

### Shipment Model
```python
- tracking_number (unique, required)
- sender_name, sender_email, sender_phone
- receiver_name, receiver_email, receiver_phone
- package_description, weight, dimensions
- origin, destination, current_location
- current_lat, current_lng (for map)
- status (auto-calculates progress)
- estimated_delivery
- created_at, updated_at (auto)
- to_dict() → JSON for API
```

### ShipmentEvent Model
```python
- shipment (ForeignKey - one-to-many)
- status
- location
- notes
- latitude, longitude
- timestamp (auto-filled)
- to_dict() → JSON for API
```

---

## 🔗 API Endpoints

### Get Full Shipment
```
GET /api/shipment/TTCP123456789/

Response:
{
    "tracking_number": "TTCP123456789",
    "status": "in_transit",
    "progress": 50,
    "origin": "New York, USA",
    "destination": "Los Angeles, USA",
    "current_lat": 40.7128,
    "current_lng": -74.0060,
    "sender_name": "Smith Industries",
    "receiver_name": "Johnson & Co.",
    "receiver_phone": "+1 (555) 123-4567",
    "package_description": "Electronics",
    "est_delivery": "01/22/2026",
    "created_at": "01/18/2026 10:30",
    "events": [
        {
            "status": "Picked Up",
            "location": "New York Hub",
            "timestamp": "01/18/2026 10:30",
            "description": "Package pickup from sender"
        },
        ...
    ]
}
```

### Get Location Only
```
GET /api/shipment/TTCP123456789/location/

Response:
{
    "tracking_number": "TTCP123456789",
    "current_lat": 40.7128,
    "current_lng": -74.0060,
    "status": "in_transit",
    "progress": 50.0
}
```

### List All Shipments
```
GET /api/shipments/?page=1&limit=20

Response:
{
    "total": 5,
    "page": 1,
    "limit": 20,
    "shipments": [...]
}
```

---

## 📁 Project Structure

```
TTT-PROJECT/
├── manage.py
├── db.sqlite3              (database)
├── requirements.txt
│
├── tracking_site/          (main Django project)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── tracking/               (tracking app - CORE)
│   ├── models.py           (✨ Shipment, ShipmentEvent)
│   ├── views.py            (✨ API endpoints)
│   ├── admin.py            (✨ Admin interface)
│   ├── urls.py             (✨ API routes)
│   └── migrations/
│
├── templates/
│   ├── index.html
│   ├── track.html          (✨ API-driven)
│   ├── signin.html
│   └── signup.html
│
└── Documentation/
    ├── SETUP_GUIDE.md              (Complete setup)
    ├── ADMIN_QUICKSTART.md         (Quick reference)
    ├── TECHNICAL_ARCHITECTURE.md   (Technical details)
    ├── IMPLEMENTATION_SUMMARY.md   (What was built)
    └── VERIFICATION_CHECKLIST.md   (Testing guide)
```

---

## 🧪 Testing

### Create Test Shipment
1. Go to `http://localhost:8000/admin/`
2. Shipments → Add Shipment
3. Enter tracking number: `TEST001`
4. Fill in some fields (or use defaults)
5. Save

### Add Test Events
1. Shipment Events → Add Event
2. Select shipment: TEST001
3. Status: "Shipped"
4. Location: "New York"
5. Save (add 2-3 more events)

### View on Tracking Page
Visit: `http://localhost:8000/track/?q=TEST001`

You should see:
- ✓ Tracking number
- ✓ Status with icon
- ✓ Progress bar (auto-calculated)
- ✓ All shipment details
- ✓ Complete timeline
- ✓ Interactive map

---

## 🔒 Security

### Public Access
- ✅ Tracking page is public (anyone can track)
- ✅ API endpoints are read-only (no modification)
- ✅ No authentication required for tracking

### Admin Access
- 🔒 Admin interface at `/admin/` requires login
- 🔒 Only staff can create/edit/delete data
- 🔒 User credentials for admin access only

---

## 📖 Documentation

Complete documentation is provided:

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Full setup instructions and workflows
- **[ADMIN_QUICKSTART.md](ADMIN_QUICKSTART.md)** - Quick reference for admins
- **[TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md)** - Detailed architecture
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Implementation details
- **[VERIFICATION_CHECKLIST.md](VERIFICATION_CHECKLIST.md)** - Testing checklist

---

## 🛠️ Troubleshooting

### Problem: "Tracking number not found"
**Solution**: Create the shipment in admin first. Tracking numbers are case-sensitive.

### Problem: Map not displaying
**Solution**: Set `current_lat` and `current_lng` in the shipment record.

### Problem: Events not showing
**Solution**: Create ShipmentEvent records and link them to the shipment.

### Problem: Django won't start
**Solution**: Run migrations: `python manage.py migrate`

---

## 🎯 Key Features Implemented

✅ **Admin Interface**: Full CRUD for shipments and events  
✅ **API Endpoints**: RESTful endpoints returning JSON  
✅ **Database Models**: Complete data persistence  
✅ **Frontend Integration**: track.html fetches real data from API  
✅ **Error Handling**: Graceful error display for invalid tracking  
✅ **Auto-Calculation**: Progress auto-calculated from status  
✅ **Interactive Map**: Leaflet.js integration with coordinates  
✅ **Timeline View**: Complete event history visualization  
✅ **Responsive Design**: Works on all device sizes  
✅ **No Sample Data**: All hardcoded demo data removed  

---

## 🚀 Deployment

### For Production
1. Change `DEBUG = False` in settings.py
2. Use PostgreSQL instead of SQLite
3. Deploy with Gunicorn + Nginx
4. Add HTTPS/SSL
5. Enable security headers
6. Set up error logging
7. Configure static files serving

See [TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md) for details.

---

## 📞 Support

For issues or questions, refer to:
- Documentation files (listed above)
- Django admin interface (intuitive design)
- API endpoints (well-structured JSON)
- Browser console (for frontend errors)

---

## 📝 License

Part of TTCP Worldwide Tracking System project.

---

## ✨ Summary

This is a **complete, production-ready tracking system** where:

1. **Admins** manually enter ALL shipment data in the Django admin interface
2. **Data** is stored in database (SQLite)
3. **API** serves the data as JSON
4. **Customers** see real data on the tracking page
5. **No sample data** - everything is live and manageable

**Start using it today!** 🎉

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then visit: `http://localhost:8000/admin/`

