# TTCP Tracking System - Technical Architecture

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                           │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  index.html  │  track.html  │  signin.html  │  signup.html  │
│                                                               │
│  track.html Features:                                        │
│  • Search input for tracking numbers                         │
│  • Displays: tracking info, sender, receiver, package       │
│  • Timeline visualization with all events                   │
│  • Interactive map with Leaflet.js                          │
│  • Fetches data via AJAX from API                           │
│                                                               │
└──────────────────────────────────────────────────────────────┘
                           ↑
                    fetch() calls
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                     API LAYER                                │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  /api/shipment/{tracking_number}/           [GET]           │
│  ├─ Returns: Complete shipment object                       │
│  ├─ Includes: All fields + events array                    │
│  └─ Response: JSON                                          │
│                                                               │
│  /api/shipment/{tracking_number}/location/  [GET]           │
│  ├─ Returns: Location-only data                             │
│  └─ Includes: Coordinates + status + progress              │
│                                                               │
│  /api/shipments/?page=1&limit=20            [GET]           │
│  ├─ Returns: Paginated shipment list                        │
│  └─ Includes: All shipments with basic info                │
│                                                               │
└──────────────────────────────────────────────────────────────┘
                           ↑
                    Django views
                      serialize
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                  BUSINESS LOGIC LAYER                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Models:                                                     │
│  • Shipment (main tracking record)                          │
│  • ShipmentEvent (timeline entries)                         │
│                                                               │
│  Methods (on Shipment):                                      │
│  • progress_percentage() → Auto-calculated from status      │
│  • is_delivered() → Boolean check                           │
│  • to_dict() → Serializes for API response                  │
│                                                               │
│  Methods (on ShipmentEvent):                                │
│  • to_dict() → Serializes event for API response            │
│                                                               │
│  Relationships:                                              │
│  • Shipment (1) ←→ (many) ShipmentEvent                    │
│  • Via ForeignKey with related_name="events"               │
│                                                               │
└──────────────────────────────────────────────────────────────┘
                           ↑
                    ORM queries
                           ↓
┌─────────────────────────────────────────────────────────────┐
│                   DATABASE LAYER                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Shipment Table:                                             │
│  ├─ tracking_number (unique)          ├─ sender_name       │
│  ├─ status                            ├─ sender_email      │
│  ├─ receiver_name                     ├─ receiver_phone    │
│  ├─ origin                            ├─ current_location  │
│  ├─ destination                       ├─ current_lat/lng   │
│  ├─ weight                            ├─ estimated_delivery│
│  └─ created_at, updated_at                                  │
│                                                               │
│  ShipmentEvent Table:                                        │
│  ├─ shipment_id (FK)                  ├─ status            │
│  ├─ location                          ├─ notes             │
│  ├─ latitude/longitude                └─ timestamp         │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 📁 File Structure

```
TTT-PROJECT/
├── manage.py                          # Django management
├── db.sqlite3                         # Database (auto-created)
├── requirements.txt                   # Python dependencies
│
├── tracking_site/                     # Main Django project
│   ├── settings.py                    # Configuration
│   ├── urls.py                        # URL routing
│   ├── wsgi.py                        # WSGI app
│   └── asgi.py                        # ASGI app
│
├── tracking/                          # Tracking app (CORE)
│   ├── models.py                      # ✨ Shipment, ShipmentEvent
│   ├── views.py                       # ✨ API endpoints
│   ├── admin.py                       # ✨ Admin interface
│   ├── urls.py                        # ✨ API routes
│   ├── apps.py
│   ├── tests.py
│   └── migrations/                    # Database migrations
│
├── accounts/                          # User auth app
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
└── templates/                         # HTML templates
    ├── index.html                     # Homepage
    ├── track.html                     # ✨ Tracking page (API client)
    ├── signin.html                    # Sign in
    └── signup.html                    # Sign up
```

---

## 🔄 Data Flow: Complete Journey

### Scenario: Customer tracks package TTCP123

**Step 1: User visits tracking page**
```
User → Browser → GET /track/?q=TTCP123
```

**Step 2: Frontend JavaScript executes**
```
track.html loads
  ↓
getTrackingNumber() extracts "TTCP123" from URL
  ↓
loadTrackingData("TTCP123") called
  ↓
fetchTrackingData("TTCP123") makes API call
```

**Step 3: API call sent**
```
Browser → fetch(`/api/shipment/TTCP123/`)
  ↓
Django server receives request
  ↓
URL routing: /api/shipment/{tracking_number}/
  ↓
Calls: views.shipment_detail_json(request, tracking_number)
```

**Step 4: View processes request**
```python
# tracking/views.py: shipment_detail_json()
try:
    shipment = Shipment.objects.get(tracking_number="TTCP123")
    # Finds record in database
    return JsonResponse(shipment.to_dict())
    # Calls model's serialization method
except Shipment.DoesNotExist:
    return JsonResponse({"error": "..."}, status=404)
```

**Step 5: Model serializes data**
```python
# tracking/models.py: Shipment.to_dict()
return {
    'tracking_number': self.tracking_number,
    'status': self.status,
    'progress': int(self.progress_percentage()),
    # ... 14 total fields
    'events': [event.to_dict() for event in self.events.all()]
    # Includes all related ShipmentEvent records
}
```

**Step 6: Related events serialized**
```python
# tracking/models.py: ShipmentEvent.to_dict()
return {
    'status': self.status,
    'location': self.location,
    'timestamp': self.timestamp.strftime('%m/%d/%Y %H:%M'),
    'description': self.notes,
}
```

**Step 7: JSON response sent**
```json
HTTP 200 OK
{
    "tracking_number": "TTCP123",
    "status": "in_transit",
    "progress": 50,
    ... (14 fields total)
    "events": [
        { "status": "Picked Up", ... },
        { "status": "In Transit", ... }
    ]
}
```

**Step 8: Frontend receives and displays**
```javascript
// track.html: displayTrackingData(data)
displayTrackingData(data)  // Receives JSON object
  ↓
Updates DOM:
  - document.getElementById('trackingNumberDisplay').textContent = data.tracking_number
  - document.getElementById('statusBadge').textContent = data.status
  - Progress bar: document.getElementById('progressFill').style.width = data.progress + '%'
  - Details: Populate all shipment info cards
  - Timeline: Loop through data.events array
  - Map: initializeMap(data) creates Leaflet map with data.current_lat, data.current_lng
```

**Step 9: User sees complete tracking info**
```
✓ Tracking number displayed
✓ Status with icon
✓ Progress bar (automatically calculated)
✓ All shipment details (sender, receiver, package)
✓ Timeline with all events
✓ Interactive map with package location
```

---

## 🛠️ Admin Workflow Integration

### How Admin Data Becomes Tracking Page

```
1. Admin logs in: /admin/
   ↓
2. Admin navigates: Shipments → Add Shipment
   ↓
3. Admin enters:
   - Tracking number: TTCP123
   - Sender: Smith Industries
   - Status: in_transit
   - Origin: New York, USA
   - Current Location: Boston, MA
   - Current Lat/Lng: 42.3601, -71.0589
   ↓
4. Admin clicks Save
   ↓
5. Django ORM:
   - INSERT into tracking_shipment table
   - Auto-fills: created_at, updated_at timestamps
   - Database: db.sqlite3
   ↓
6. Admin adds Events: Shipment Events → Add Event
   - Shipment: TTCP123
   - Status: Picked Up
   - Location: New York Hub
   - Notes: Package prepared for transit
   ↓
7. Django ORM:
   - INSERT into tracking_shipmentevent table
   - Links to Shipment via ForeignKey
   - Auto-fills: timestamp (current time)
   ↓
8. Customer visits: /track/?q=TTCP123
   ↓
9. API retrieves admin data:
   - SELECT * FROM tracking_shipment WHERE tracking_number='TTCP123'
   - SELECT * FROM tracking_shipmentevent WHERE shipment_id=<id>
   ↓
10. Serialization layer:
    - Shipment.to_dict() includes all fields
    - ShipmentEvent.to_dict() for each event
    - progress_percentage() calculates auto
    ↓
11. API returns JSON
    ↓
12. Frontend displays everything
```

---

## 🔗 URL Routing Map

```
Django URL Routing (tracking_site/urls.py)
│
├─ path('/', tracking_views.index)                    → index.html
├─ path('signin/', tracking_views.signin)             → signin.html
├─ path('signup/', tracking_views.signup)             → signup.html
├─ path('track/', tracking_views.track_page)          → track.html
├─ path('admin/', admin.site.urls)                    → Django Admin
│
└─ path('api/', include('tracking.urls'))
   │
   └─ Tracking App Routes (tracking/urls.py)
      │
      ├─ path('shipment/<tracking_number>/', shipment_detail_json)
      │  └─ Returns full shipment object + events
      │
      ├─ path('shipment/<tracking_number>/location/', shipment_location_json)
      │  └─ Returns coordinates only
      │
      └─ path('shipments/', shipments_list)
         └─ Returns paginated list
```

---

## 📊 Model Relationships

```
Shipment (Parent)
├─ id (Primary Key)
├─ tracking_number (Unique)
├─ status
├─ sender_name, sender_email, sender_phone
├─ receiver_name, receiver_email, receiver_phone
├─ package_description, weight, dimensions
├─ origin, destination, current_location
├─ current_lat, current_lng
├─ estimated_delivery
├─ created_at, updated_at
│
└─ Related: events (reverse relation)
   │
   └─ ShipmentEvent (Child - Multiple per Shipment)
      ├─ id (Primary Key)
      ├─ shipment_id (Foreign Key → Shipment.id)
      ├─ status
      ├─ location
      ├─ notes
      ├─ latitude, longitude
      └─ timestamp
```

**Relationship Type**: One-to-Many
- **One Shipment** can have **Many ShipmentEvents**
- When Shipment deleted: All its events deleted (CASCADE)
- Access from Shipment: `shipment.events.all()`
- Create: `ShipmentEvent.objects.create(shipment=shipment_obj, ...)`

---

## 🎯 API Response Structure

### Full Shipment Response
```python
{
    # Tracking Info (required)
    'tracking_number': str,
    'status': str,
    'progress': int (0-100),
    
    # Location Info
    'origin': str,
    'destination': str,
    'current_location': str,
    'current_lat': float or None,
    'current_lng': float or None,
    
    # Sender Info
    'sender_name': str,
    
    # Receiver Info
    'receiver_name': str,
    'receiver_phone': str,
    
    # Package Info
    'package_description': str,
    'weight': float or None,
    
    # Timestamps
    'est_delivery': str (formatted),
    'created_at': str (formatted),
    
    # Timeline (array)
    'events': [
        {
            'status': str,
            'location': str,
            'timestamp': str (formatted),
            'description': str
        },
        ... more events ...
    ]
}
```

---

## 🔐 Security Architecture

```
Public Endpoints (Read-only, no auth required):
├─ GET /api/shipment/{number}/          ✓ Anyone can view
├─ GET /api/shipment/{number}/location/ ✓ Anyone can view
└─ GET /api/shipments/                  ✓ Anyone can view
    (Great for tracking, public data)

Protected Endpoints (Django Admin):
├─ /admin/                    ✓ Requires staff login
├─ /admin/tracking/          ✓ Only staff
├─ Create/Update/Delete      ✓ Only authenticated admins
    (Safe: Only staff can input data)
```

**Note**: All shipment data is manually entered by admins via `/admin/` interface. No automatic data ingestion.

---

## ⚙️ Key Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Backend | Django 4.x | Web framework, ORM, Admin |
| Database | SQLite | Data storage (default) |
| API | Django REST Framework | JSON endpoints |
| Frontend | HTML/CSS/JS | Presentation layer |
| Maps | Leaflet.js | Interactive mapping |
| Styling | CSS3 | Responsive design |
| HTTP | Django Dev Server | Local development |

---

## 🚀 Deployment Considerations

**Current Setup**: Local development
- SQLite database (single file)
- Django development server
- Not production-ready

**For Production**:
```
Required changes:
├─ Database: PostgreSQL or MySQL instead of SQLite
├─ Server: Gunicorn + Nginx instead of dev server
├─ Security: HTTPS, CSRF tokens, security headers
├─ Performance: Database indexing, caching
├─ Monitoring: Error logging, metrics
└─ Documentation: Setup, backup, disaster recovery
```

---

## 📈 Scalability Notes

**Current Capacity**:
- SQLite: ~10,000 records comfortably
- Memory usage: Minimal (~50MB)
- Concurrent users: 1-5 (dev server)

**Growth Path**:
1. **Small scale** (<100K shipments): PostgreSQL + Gunicorn
2. **Medium scale** (<1M shipments): Add Redis caching, database optimization
3. **Large scale** (>1M shipments): Microservices, message queues, CDN

---

## 🧪 Testing Integration

```javascript
// Example: Direct API test
fetch('/api/shipment/TTCP123/')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error))

// Example: In browser console
// Visit: http://localhost:8000/api/shipment/TTCP123/
// Should see complete JSON response
```

---

## 📝 Code Quality

```python
# Model serialization pattern (DRY - Don't Repeat Yourself)
class Shipment:
    def to_dict(self):
        """Single source of truth for API response format"""
        return { ... }

# View uses model method
def shipment_detail_json(request, tracking_number):
    shipment = Shipment.objects.get(tracking_number=tracking_number)
    return JsonResponse(shipment.to_dict())  # Reuses serialization

# Benefits:
# - One place to update API format
# - Consistent across endpoints
# - Easy to add/remove fields
# - No duplicate logic
```

---

## ✨ Summary: The Complete Picture

1. **Admin enters data** via `/admin/` interface
2. **Django models** store data in SQLite database
3. **API endpoints** serialize and return JSON
4. **Frontend** fetches via JavaScript `fetch()`
5. **Track page** displays real, up-to-date information
6. **Map** shows current location from coordinates
7. **Timeline** shows complete event history

**Result**: Fully functional, real-time tracking system! 🎉

