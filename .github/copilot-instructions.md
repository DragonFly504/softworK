# AI Coding Agent Instructions for TTCP Tracking System

## Project Overview

**TTCP Worldwide** is a Django-based logistics tracking system with:
- Backend: Django admin interface for manual shipment data entry
- Frontend: Public tracking page with real-time status and interactive map
- API: RESTful JSON endpoints (read-only from frontend)
- Architecture: Admin-driven data input → Database → API → Frontend visualization

**Key principle**: No automated data ingestion—admins manually create all shipment records in Django admin.

---

## Architecture & Data Flow

### Three-Layer Architecture

```
Django Admin (Data Entry) → SQLite/PostgreSQL → REST API → Frontend (tracking.html)
```

**Shipment Lifecycle**:
1. Admin creates `Shipment` record in `/admin/tracking/shipment/`
2. Admin creates `ShipmentEvent` records (timeline entries) for each status update
3. Frontend calls API endpoint `/api/shipment/{tracking_number}/`
4. Data serialized via `to_dict()` methods in models
5. Frontend renders map, timeline, and shipment details

### Critical Files for Understanding Data Flow

- **[tracking/models.py](tracking/models.py)**: `Shipment` (main record) and `ShipmentEvent` (timeline). Both have `to_dict()` methods for serialization.
- **[tracking/views.py](tracking/views.py)**: API endpoints that query models and return `JsonResponse`. Key views: `shipment_detail_json()`, `shipment_location_json()`.
- **[tracking/admin.py](tracking/admin.py)**: Fieldsets organization for admin UI. Configure display order and grouping here.
- **[templates/track.html](templates/track.html)**: Frontend client using `fetch()` to call API. Uses Leaflet.js for maps.

---

## Project Structure

```
TTT-PROJECT/
├── manage.py                         # Django CLI entry point
├── requirements.txt                  # Python dependencies (Django, Pillow, phonenumber-field, etc.)
├── tracking_site/                    # Django project config
│   ├── settings.py                   # Database, installed apps, middleware
│   ├── urls.py                       # Main URL router
│   └── wsgi.py                       # Production entry point
├── tracking/                         # CORE APP - All tracking logic
│   ├── models.py                     # Shipment & ShipmentEvent models
│   ├── views.py                      # API views returning JSON
│   ├── admin.py                      # Admin interface customization
│   ├── urls.py                       # API route definitions
│   └── migrations/                   # Database schema versions
├── accounts/                         # User authentication (auth system)
├── templates/
│   ├── track.html                    # ⭐ Main tracking page (API client)
│   ├── index.html, signin.html, signup.html  # Other pages
├── static/
│   ├── css/                          # Stylesheets
│   └── js/                           # JavaScript (Leaflet.js for maps)
└── [Documentation files]             # README.md, SETUP_GUIDE.md, etc.
```

---

## Common Development Workflows

### To Add a New Shipment Field

1. **Model**: Add field to `Shipment` model in `tracking/models.py`
2. **Migration**: Run `python manage.py makemigrations tracking`
3. **Admin**: Add field to `ShipmentAdmin` fieldsets in `tracking/admin.py`
4. **Serialization**: Add field to `to_dict()` method in `Shipment` model
5. **Frontend**: Update `templates/track.html` to display new field

**Example**: Adding `insurance_value` field:
```python
# models.py
insurance_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

# admin.py - add to ShipmentAdmin fieldsets
'Package Details': {'fields': ('package_description', 'weight', 'dimensions', 'insurance_value')}

# models.py - add to to_dict()
'insurance_value': self.insurance_value
```

### To Create a New API Endpoint

1. **View**: Create function in `tracking/views.py` returning `JsonResponse`
2. **URL**: Add route in `tracking/urls.py` using `path()` or `re_path()`
3. **Response Format**: Use model's `to_dict()` for consistency

**Example**:
```python
# views.py
def shipment_summary(request, tracking_number):
    shipment = Shipment.objects.get(tracking_number=tracking_number)
    return JsonResponse({'status': shipment.status, 'progress': shipment.progress_percentage()})

# urls.py
path('api/summary/<str:tracking_number>/', shipment_summary, name='api_summary')
```

### To Test API Locally

```bash
# Start server
python manage.py runserver

# Test endpoint in browser or curl
curl http://localhost:8000/api/shipment/ABC123456/

# Admin panel
http://localhost:8000/admin/
# Create test shipment via admin UI
# Then visit http://localhost:8000 and track it
```

---

## Key Conventions & Patterns

### Model Serialization Pattern
All models use `to_dict()` method for API responses (not DRF serializers). This keeps JSON structure transparent and easy to modify.

```python
def to_dict(self):
    return {
        'field1': self.field1,
        'field2': self.field2,
    }
```

### Status Choices
Defined as tuples in model—used in admin dropdowns and frontend logic:
```python
STATUS_CHOICES = [
    ("created", "Created"),
    ("in_transit", "In Transit"),
    ("delivered", "Delivered"),
]
```

### Admin Fieldsets
Organize fields by logical groups—affects what admins see in form:
```python
fieldsets = (
    ('Shipment Info', {'fields': ('tracking_number', 'status')}),
    ('Sender', {'fields': ('sender_name', 'sender_email')}),
)
```

### Frontend API Calls
All data fetching via vanilla `fetch()` (no jQuery). Parse JSON and render templates:
```javascript
fetch(`/api/shipment/${trackingNumber}/`)
    .then(r => r.json())
    .then(data => renderTrackingDetails(data))
```

---

## Database Schema Quick Reference

### Shipment Table
| Field | Type | Purpose |
|-------|------|---------|
| tracking_number | CharField | Unique ID for shipment |
| status | CharField | One of: created, in_transit, out_for_delivery, delivered, failed |
| sender_name, sender_email, sender_phone | Text | Origin contact |
| receiver_name, receiver_email, receiver_phone | Text | Destination contact |
| origin, destination | CharField | City/address |
| origin_lat, origin_lng, dest_lat, dest_lng | Float | Map coordinates |
| current_lat, current_lng, current_location | Float/Text | Real-time position |
| weight, dimensions | Float/Text | Package specs |
| created_at, updated_at | DateTime | Timestamps |

### ShipmentEvent Table (Timeline)
| Field | Type | Purpose |
|-------|------|---------|
| shipment | ForeignKey | Links to Shipment |
| status | CharField | Event status (same choices as Shipment) |
| location | CharField | Where event occurred |
| latitude, longitude | Float | Event coordinates |
| notes | TextField | Event description |
| timestamp | DateTime | When event occurred |

---

## Integration Points

### Django Admin → API
Admin form saves → Triggers model's `save()` method → Database updated → API `to_dict()` reads from database → Frontend fetches fresh data.

### Frontend → Map Display
`track.html` uses **Leaflet.js** with OpenStreetMap tiles. Coordinates come from API:
```javascript
const shipment = await fetch(`/api/shipment/${num}/`).then(r => r.json());
const marker = L.marker([shipment.current_lat, shipment.current_lng]).addTo(map);
```

### Search & Timeline
Frontend searches tracking numbers via text input. Each `ShipmentEvent` renders as timeline entry using `to_dict()` serialization.

---

## External Dependencies

- **Django 4.x/5.x**: Web framework
- **Leaflet.js**: Map visualization (frontend)
- **Pillow**: Image handling for profile pictures
- **django-phonenumber-field**: Phone validation
- **python-decouple**: Environment configuration
- **PostgreSQL** (optional): Production database

---

## Configuration & Environment

**Key settings in `settings.py`**:
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Add production domain
- `DATABASES`: Configure PostgreSQL for production (defaults to SQLite)
- `SECRET_KEY`: Change from default before deploying

**Environment variables** (in `.env` or system):
- `SECRET_KEY`: Django secret
- `DEBUG`: True/False
- `DATABASE_URL` (optional): For production

---

## Testing & Validation

**Before committing changes**:
```bash
python manage.py makemigrations --dry-run  # Check migrations won't break
python manage.py check                     # Verify Django config
python manage.py test                      # Run unit tests (if written)
```

**Manual verification**:
1. Create test shipment in admin
2. Verify API response via `curl` or browser
3. Test frontend search and map display
4. Check edge cases (invalid tracking number, empty fields)

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| API returns 404 | Check `tracking_number` case sensitivity; ensure shipment exists in DB |
| Map not loading | Verify latitude/longitude are valid floats; check Leaflet.js CDN in HTML |
| Admin not showing field | Add to `ShipmentAdmin.fieldsets` in `admin.py` |
| Migration conflicts | Delete migration file, re-run `makemigrations` |
| CORS errors | If frontend on different domain, add to `CORS_ALLOWED_ORIGINS` |

---

## Documentation Files (Read in Order)

1. **README.md**: Project overview + quick start (5 min)
2. **ADMIN_QUICKSTART.md**: Admin workflow reference (5 min)
3. **TECHNICAL_ARCHITECTURE.md**: Deep dive into system design (20 min)
4. **SETUP_GUIDE.md**: Field reference + API examples (15 min)

---

## Key Files to Modify When Adding Features

| Goal | Modify |
|------|--------|
| Add shipment field | `models.py` (field), `admin.py` (UI), `to_dict()` (API) |
| Create new API | `views.py`, `urls.py` |
| Change admin layout | `admin.py` (fieldsets) |
| Update frontend | `templates/track.html`, `static/js/*.js` |
| Change status types | `models.py` (STATUS_CHOICES) |

---

## Deployment Notes

- **Local**: `python manage.py runserver` on port 8000
- **Production**: Use Gunicorn + Nginx + PostgreSQL + HTTPS
- **Static files**: Collect with `python manage.py collectstatic`
- **Database**: Run migrations with `python manage.py migrate` before launch

---

## Quick Commands Reference

```bash
# Setup
python manage.py migrate                    # Apply DB migrations
python manage.py createsuperuser            # Create admin account
python manage.py runserver                  # Start dev server

# Development
python manage.py makemigrations             # Create migration files
python manage.py shell                      # Django Python shell
python manage.py dbshell                    # Database shell

# Admin
# Access at http://localhost:8000/admin/

# Testing
python manage.py test tracking              # Run tests for tracking app
```

---

## When in Doubt

1. **Architecture question?** → Read `TECHNICAL_ARCHITECTURE.md`
2. **Admin workflow?** → Check `ADMIN_QUICKSTART.md`
3. **API endpoints?** → Look at `tracking/urls.py` + `tracking/views.py`
4. **Database schema?** → Check `tracking/models.py`
5. **Frontend code?** → Check `templates/track.html` + `static/js/`
