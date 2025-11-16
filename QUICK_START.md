# Quick Start Guide - Military Base Access Control

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies
Open PowerShell in the project folder and run:

```powershell
pip install -r requirements.txt
```

### Step 2: Run the Application
```powershell
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

### Step 3: Open in Browser
Go to: **http://127.0.0.1:5000**

---

## 🔐 Demo Login (Pre-registered Faces)

The system comes with 3 demo soldiers. To test, you'll need to:

1. Click "Access Granted" on the home page
2. Choose "Capture Photo" or "Upload Photo"
3. Take a selfie or upload an image with your face
4. Click "Authenticate"

**First time?** Your face will be registered as a new soldier.

---

## 📋 Demo Accounts (Without Photos)

These accounts exist in the system:

```
Username: soldier1 (John Smith)
Username: soldier2 (Sarah Johnson)  
Username: soldier3 (Michael Davis)
```

To use these, you need to register their faces first by capturing/uploading photos while logged in.

---

## 🎯 Features to Try

### 1. Face Authentication
- Capture photo from webcam
- Or upload existing image
- System recognizes your face

### 2. Access Control
- View your profile
- See authorized areas
- Request access to areas

### 3. Admin Dashboard (TOP SECRET only)
- View access logs
- View all personnel
- Monitor system activity

---

## 🛠️ Project Files

| File | Purpose |
|------|---------|
| `app.py` | Backend Flask application |
| `requirements.txt` | Python dependencies |
| `templates/index.html` | Home page |
| `templates/login.html` | Login page |
| `templates/dashboard.html` | Dashboard |
| `static/css/style.css` | Styling |
| `static/js/login.js` | Login logic |
| `static/js/dashboard.js` | Dashboard logic |

---

## 🔧 Common Issues & Fixes

### Issue: "ModuleNotFoundError: No module named 'face_recognition'"

**Fix:**
```powershell
pip install face-recognition
```

### Issue: "Port 5000 already in use"

**Fix:** Edit `app.py` and change the port:
```python
app.run(debug=True, host='127.0.0.1', port=5001)
```

Then go to: `http://127.0.0.1:5001`

### Issue: Camera not working

**Fix:**
- Check browser camera permissions
- Allow camera access when browser asks
- Try Firefox or Chrome
- Ensure camera is not in use by another app

### Issue: Face recognition not working

**Fix:**
- Ensure good lighting
- Face should be clearly visible
- Try higher quality image
- Move closer/farther from camera

---

## 📊 System Architecture

```
User Browser
    ↓
Flask Web Server (app.py)
    ├─ Face Recognition API
    ├─ Session Management
    ├─ Access Control Logic
    └─ Personnel Database
    ↓
File Storage
    ├─ Face Encodings
    ├─ Access Logs
    └─ Personnel Data
```

---

## 🔐 Security Levels

```
CONFIDENTIAL:   Basic access (barracks, cafeteria)
SECRET:         Full access (+ armory, command center)
TOP SECRET:     Complete access (+ war room, admin panel)
```

---

## 📱 Browser Compatibility

✅ Chrome/Edge (Recommended)
✅ Firefox
✅ Safari (with limitations)
⚠️ Mobile browsers (camera access varies)

---

## 🎓 Next Steps

1. ✅ Install and run the application
2. ✅ Test face authentication
3. ✅ Explore the dashboard
4. ✅ Try admin features (if TOP SECRET)
5. ✅ Customize personnel database
6. ✅ Customize access areas

---

## 📞 Need Help?

Check `README.md` for detailed documentation or refer to the troubleshooting section above.

**Happy testing!** 🎖️

---

**Version**: 1.0.0  
**Last Updated**: November 2025
