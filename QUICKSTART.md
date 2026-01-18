# 🚀 QUICK START - 5 MINUTES TO RUNNING

> Get the TTCP Tracking System up and running in 5 minutes!

---

## ⚡ 5-Minute Setup

### Step 1: Prepare Database (1 min)
```bash
python manage.py makemigrations tracking
python manage.py migrate
```

### Step 2: Create Admin User (1 min)
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin account.

### Step 3: Start Server (1 min)
```bash
python manage.py runserver
```

### Step 4: Login to Admin (1 min)
Visit: `http://localhost:8000/admin/`
- Username: (what you entered above)
- Password: (what you entered above)

### Step 5: Create Your First Shipment (1 min)
1. Click: **Shipments** → **Add Shipment**
2. Enter:
   - **Tracking Number**: `TEST001`
   - **Status**: `in_transit`
   - Click: **Save**

---

## 🎯 Now Try It!

### Track Your Package
Visit: `http://localhost:8000/track/?q=TEST001`

**You should see:**
- ✓ Tracking number displayed
- ✓ Status badge (📦 IN TRANSIT)
- ✓ Progress bar (50%)
- ✓ Shipment info
- ✓ Map showing default location

---

## 📚 Need More Help?

### Want to add tracking events?
See: [ADMIN_QUICKSTART.md](ADMIN_QUICKSTART.md)

### Want complete setup?
See: [SETUP_GUIDE.md](SETUP_GUIDE.md)

### Want to understand the system?
See: [README.md](README.md)

### Want visual explanations?
See: [VISUAL_GUIDE.md](VISUAL_GUIDE.md)

### Want technical details?
See: [TECHNICAL_ARCHITECTURE.md](TECHNICAL_ARCHITECTURE.md)

### Want to know what was built?
See: [PROJECT_COMPLETION.md](PROJECT_COMPLETION.md)

---

## ✨ That's It!

You now have a working tracking system! 🎉

- ✅ Admin interface at `/admin/`
- ✅ Tracking page at `/track/`
- ✅ API at `/api/shipment/{number}/`

**Start entering shipment data and watch it display on the tracking page!**

---

## 💡 Common Next Steps

### Add More Shipments
```
/admin/ → Shipments → Add Shipment
(Fill in more details this time)
```

### Add Tracking Events
```
/admin/ → Shipment Events → Add Event
(Select a shipment and add status updates)
```

### View Complete Timeline
```
/track/?q=YOUR_TRACKING_NUMBER
(Should show all events you added)
```

### Test API Directly
```
http://localhost:8000/api/shipment/TEST001/
(Should return JSON with all data)
```

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Migration error | Run: `python manage.py migrate --run-syncdb` |
| Admin login fails | Make sure you ran `createsuperuser` |
| Tracking page is empty | Create shipment in admin first |
| Map doesn't show | Set current_lat and current_lng in admin |
| API returns 404 | Tracking number doesn't exist in database |

---

## 🔗 Key URLs

| What | URL |
|------|-----|
| Homepage | `http://localhost:8000/` |
| Admin Panel | `http://localhost:8000/admin/` |
| Tracking Page | `http://localhost:8000/track/` |
| Track Specific | `http://localhost:8000/track/?q=TEST001` |
| API Test | `http://localhost:8000/api/shipment/TEST001/` |

---

## 📝 Key Admin Fields

When creating a shipment, you can fill in:

**Required:**
- Tracking Number (unique ID)

**Important:**
- Status (created/in_transit/out_for_delivery/delivered/failed)
- Sender Name
- Receiver Name
- Origin (city)
- Destination (city)

**Optional:**
- All phone, email fields
- Package description
- Weight
- Coordinates (for map)
- Estimated delivery

---

## 🎉 Success!

**If you see data on the tracking page → System is working!**

---

## 📖 Next: Pick Your Path

### Path A: "Just Use It"
→ Keep entering data in admin
→ Track on the tracking page
→ That's all you need!

### Path B: "Understand It"
→ Read: README.md (10 min)
→ Read: ADMIN_QUICKSTART.md (5 min)
→ Explore: SETUP_GUIDE.md as needed

### Path C: "Deploy It"
→ Read: TECHNICAL_ARCHITECTURE.md
→ Follow: Production deployment section
→ Deploy to your server

---

## ✅ Checklist

- [ ] Ran migrations
- [ ] Created admin user
- [ ] Started server
- [ ] Logged into admin
- [ ] Created test shipment
- [ ] Visited tracking page
- [ ] Saw tracking info display
- [ ] Added tracking events
- [ ] Saw timeline update
- [ ] Tested API endpoint

**All done?** You're ready to use the system! 🚀

---

**Questions?** See the full documentation in the project folder!
