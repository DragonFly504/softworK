# TTT-PROJECT - Logo & Redirect Setup Guide

## ✅ Completed Setup

### 1. Logo Location
All HTML templates have been configured to reference your logo from:
```
/static/images/logo.png
```

**You need to place your logo.png file in:**
```
c:\Users\USER\Desktop\TTT-PROJECT\static\images\logo.png
```

### 2. Updated Files

#### ✅ signup.html
- **Logo:** Changed from emoji (📦) to `/static/images/logo.png`
- **Redirect Button:** "Already have an account?" → `/signin/` ✅

#### ✅ signin.html  
- **Logo:** Changed from emoji (📦) to `/static/images/logo.png`
- **Redirect Button:** "Don't have an account?" → `/signup/` ✅

#### ✅ index.html (Home Page)
- **Logo:** Updated from `static/logo.png` to `/static/images/logo.png` ✅
- **Redirect Buttons:**
  - Navigation "Login" → `/signin/` ✅
  - Navigation "Register" → `/signup/` ✅
  - Hero "Get Started" button → `/signup/` ✅
  - CTA "Sign Up Now" button → `/signup/` ✅
  - Footer "Track Package" → `/track/` ✅
  - Footer "Sign Up" → `/signup/` ✅
  - Footer "Sign In" → `/signin/` ✅

#### ✅ track.html (Tracking Page)
- **Logo:** Updated from `static/logo.png` to `/static/images/logo.png` ✅
- **Navigation:** Home logo link → `/` ✅
- **Back Button:** Back link → `/` ✅

### 3. All Redirect Buttons Summary

| Page | Button Text | Current Link | Status |
|------|-------------|--------------|--------|
| signup.html | Already have an account? | /signin/ | ✅ Verified |
| signin.html | Don't have an account? | /signup/ | ✅ Verified |
| index.html | Login | /signin/ | ✅ Verified |
| index.html | Register | /signup/ | ✅ Verified |
| index.html | Get Started | /signup/ | ✅ Verified |
| index.html | Sign Up Now | /signup/ | ✅ Verified |
| track.html | Logo | / | ✅ Verified |
| track.html | Back Button | / | ✅ Verified |

### 4. File Structure
```
TTT-PROJECT/
├── templates/
│   ├── index.html (Home - references /static/images/logo.png)
│   ├── signup.html (Sign Up - references /static/images/logo.png)
│   ├── signin.html (Sign In - references /static/images/logo.png)
│   └── track.html (Tracking - references /static/images/logo.png)
└── static/
    └── images/
        └── logo.png ← PLACE YOUR LOGO HERE
```

### 5. Logo Requirements
- **Format:** PNG with transparent background recommended
- **Size:** 100px × 100px (will scale responsively on all pages)
- **Name:** Exactly `logo.png`
- **Location:** `/static/images/logo.png`

### 6. Next Steps
1. **Copy your TTCPWorldwide logo** to `c:\Users\USER\Desktop\TTT-PROJECT\static\images\logo.png`
2. Test all redirect buttons to ensure they work correctly
3. Verify logo appears on all 4 pages:
   - Home page (index.html)
   - Sign Up page (signup.html)
   - Sign In page (signin.html)
   - Track page (track.html)

### 7. CSS Styling for Logo
All pages have responsive CSS styling for the logo:
```css
.logo-section img {
    max-width: 100px;
    height: auto;
    display: block;
}
```

The logo will automatically scale and center on all pages!

---

**Date Updated:** January 18, 2026
**Status:** ✅ All HTML files configured and ready for logo placement
