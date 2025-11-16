# Hawkeye  Military Base Access Control System

A modern, enterprise-grade web application for military personnel authentication and access control with an elegant face authentication interface and premium UI design.

---

## Features

- **Face Authentication**  Real-time face capture and verification system  
- **Multi-Level Clearance**  Three security levels (CONFIDENTIAL, SECRET, TOP SECRET)  
- **Personnel Management**  Secure personnel database with roles and units  
- **Area Access Control**  Granular access control to restricted base areas  
- **Officer Dashboard**  Real-time access logs and personnel oversight (admin only)  
- **Premium UI**  Modern dark theme with gold accents and smooth animations  
- **Real-Time Processing**  Instant authentication and access verification  
- **Session Management**  Secure server-side session handling with logout  

---

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Flask 3.0.3, Flask-Session 0.5.0 (Python 3.13) |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla) |
| **Image Processing** | Pillow 12.0.0 |
| **Styling** | Custom CSS with Inter font, responsive design |
| **Authentication** | MD5 hash-based face verification (demo) |
| **Storage** | Filesystem (face encodings pickle file) |
| **UI/UX** | SVG logo, scanning animation, enterprise design |

---

## Prerequisites

- **Python**: 3.13 (Microsoft Store or official distribution)
- **pip**: Python package manager
- **Browser**: Modern browser with webcam support (Chrome, Firefox, Edge)
- **Webcam**: For face capture (or use photo upload)
- **OS**: Windows, macOS, or Linux

---

## Quick Start

### 1. Navigate to Project
```powershell
cd "C:\Users\ev208\OneDrive\Desktop\Projects\305HackNov\military-base-access-control"
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Start Flask Server
```powershell
python app.py
```

Expected output:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

### 4. Open in Browser
- **Home**: http://127.0.0.1:5000
- **Login**: http://127.0.0.1:5000/login
- **Dashboard**: http://127.0.0.1:5000/dashboard

---

## Project Structure

```
military-base-access-control/
 app.py                          # Flask backend (routes, API, auth)
 requirements.txt                # Python dependencies
 README.md                       # This file
 QUICK_START.md                 # Quick reference guide
 run.bat                         # Windows batch start script

 templates/
    index.html                 # Landing page with hero + features
    login.html                 # Authentication page (webcam/upload)
    dashboard.html             # User dashboard (profile, logs, admin)

 static/
    css/
       style.css              # Unified theme (Hawkeye brand colors)
    js/
       main.js                # Global scripts
       login.js               # Face capture & scanning animation
       dashboard.js           # Dashboard interactivity
    images/
        hawkeye-logo.svg       # Professional eye logo

 uploads/
    authorized_faces/          # Stored authorized face photos

 flask_session/                 # Session storage (auto-created)
```

---

## Usage Guide

### First Login (Register Face)

1. Open http://127.0.0.1:5000/login
2. **Option A  Webcam Capture**:
   - Click "Capture Photo" tab
   - Allow camera permissions in browser
   - Position your face in the frame
   - Click "Capture" button
   - Click "Authenticate" to submit

3. **Option B  Upload Photo**:
   - Click "Upload Photo" tab
   - Drag & drop or browse for an image
   - Click "Authenticate" to submit

4. On first login, your face is registered as soldier1

### Dashboard Features

- **Personnel Profile**  View rank, unit, clearance level
- **Access Areas**  View authorized areas for your clearance
- **Request Area Access**  Test access to different areas
- **Admin Console** (TOP SECRET clearance only):
  - View complete access logs
  - View all personnel database

---

## Demo Personnel

| ID | Name | Rank | Unit | Clearance | Access |
|---|---|---|---|---|---|
| soldier1 | John Smith | Captain | Alpha Squadron | SECRET | barracks, armory, command_center |
| soldier2 | Sarah Johnson | Lieutenant | Bravo Squadron | TOP SECRET | barracks, armory, command_center, war_room |
| soldier3 | Michael Davis | Sergeant | Charlie Squadron | CONFIDENTIAL | barracks, cafeteria |

**First login registers as soldier1 by default.**

---

## API Endpoints

### Authentication
- POST /api/authenticate - Authenticate user via face
- POST /api/register-face - Register new face for soldier
- GET /api/check-session - Check current session status
- POST /api/logout - Clear session and logout

### Profile (requires login)
- GET /api/profile - Get current user profile
- POST /api/request-access - Check/request access to area

### Admin (TOP SECRET clearance only)
- GET /api/access-log - View access logs
- GET /api/all-personnel - View all personnel

---

## UI/UX Design

### Hawkeye Branding
- **Primary Color**: Navy (#071226)
- **Accent Color**: Hawk Gold (#ffb400)
- **Secondary Dark**: #0d2536
- **Typography**: Inter (Google Fonts)

### Key Features
- Responsive grid layouts (3-col desktop, 2-col tablet, 1-col mobile)
- Smooth animations and hover effects
- Enterprise aerospace-inspired design
- Full-screen scanning animation during authentication
- Professional SVG logo with realistic eye design

---

## Configuration

### Change Port

Edit app.py, last line:
```python
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)  # Change 5000 to 5001
```

Then restart: python app.py

### Add Personnel

Edit app.py, modify PERSONNEL_DB:
```python
PERSONNEL_DB = {
    'new_soldier': {
        'name': 'Full Name',
        'rank': 'Rank',
        'unit': 'Unit Name',
        'clearance_level': 'SECRET',
        'access_areas': ['barracks', 'armory'],
    },
}
```

### Add Access Areas

1. Add to personnel access_areas lists
2. Update dropdown in templates/dashboard.html (Request Area Access section)
3. Update validation in app.py /api/request-access route

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Browser shows "Connection Refused" | Ensure Flask is running; check console shows "Running on http://127.0.0.1:5000" |
| Camera not working | Allow browser permissions; test camera in system settings; try Firefox/Chrome |
| Face auth fails | Good lighting required; face should be centered and clear; try uploading a photo instead |
| Python module errors | Run pip install --upgrade pip then pip install -r requirements.txt |
| Port 5000 in use | Use netstat -ano \| findstr :5000 to find PID, then taskkill /PID <PID> /F |
| CSS changes not appearing | Hard refresh browser: Ctrl+Shift+R (clears cache) |
| Session lost after refresh | Normal behavior; restart Flask to clear sessions |

---

## Security Notes

- **Face Encoding**: Uses MD5 hash of grayscale image for demo purposes
- **Session Storage**: Server-side via Flask-Session (filesystem in demo)
- **Access Logs**: All access attempts logged with timestamp and status
- **Clearance Levels**: TOP SECRET users have access to admin endpoints
- **HTTPS**: Production deployment requires SSL/TLS encryption

WARNING: This is a demonstration system. Do NOT use for real military applications without proper security hardening.

---

## File Descriptions

| File | Purpose |
|------|---------|
| app.py | Main Flask app with routes, API endpoints, authentication logic |
| requirements.txt | Python package dependencies (Flask, Pillow, etc.) |
| index.html | Landing page (hero, features, system overview) |
| login.html | Authentication page (webcam capture or photo upload) |
| dashboard.html | User dashboard (profile, access areas, admin console) |
| style.css | Unified CSS theme with Hawkeye branding and responsive design |
| login.js | Client-side auth logic and scanning animation |
| dashboard.js | Dashboard interactivity (access requests, admin panel) |
| hawkeye-logo.svg | Professional SVG logo (integrated in navbar) |

---

## Advanced Usage

### Run with Different Python Version
```powershell
# If multiple Python versions installed
py -3.13 app.py
```

### Debug Mode
Server runs in debug mode by default. Changes to files auto-reload.

### Disable Debug (for production testing)
```python
app.run(debug=False, host='127.0.0.1', port=5000)
```

### Access from Another Machine (same network)
1. Find your machine's IP: ipconfig  look for "IPv4 Address"
2. Start Flask: python app.py --host 0.0.0.0 --port 5000
3. From other machine: http://<YOUR_IP>:5000

---

## API Examples (cURL)

```bash
# Check session
curl http://127.0.0.1:5000/api/check-session

# Authenticate (requires multipart image)
curl -X POST -F "image=@face.jpg" http://127.0.0.1:5000/api/authenticate

# Get profile (requires login)
curl -b cookies.txt http://127.0.0.1:5000/api/profile

# Request access to area
curl -X POST -H "Content-Type: application/json" \
  -d '{"area":"armory"}' \
  -b cookies.txt http://127.0.0.1:5000/api/request-access
```

---

## Learning Resources

- Flask Docs: https://flask.palletsprojects.com/
- Pillow Docs: https://pillow.readthedocs.io/
- HTML/CSS/JS: https://developer.mozilla.org/
- REST API Design: https://restfulapi.net/

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | Nov 2025 | Initial release with Hawkeye branding, premium UI, face auth system |

---

## Support

For issues or questions:
1. Check this README and QUICK_START.md
2. Review Flask output logs in terminal
3. Check browser console (F12  Console tab)
4. Verify all files are in correct locations

---

**Hawkeye  Enterprise-Grade Military Access Control**

Secure. Professional. Powerful.

---

Last Updated: November 15, 2025
Project Version: 1.0.0
Maintained by: Development Team
