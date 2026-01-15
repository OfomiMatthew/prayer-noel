# 🎄 Pray Noel - Quick Start Guide

## Welcome to Pray Noel!

This is your comprehensive Christmas Prayer Request Platform built with Flask, SQLite, and Tailwind CSS.

## 🚀 Quick Start

### 1. The app is already set up and running!

The Flask development server should be running at:

- **http://localhost:5000** or **http://127.0.0.1:5000**

### 2. Login with Sample Accounts

The database has been seeded with sample data. You can login with:

**Admin Account:**

- Email: `admin@praynoel.com`
- Password: `admin123`
- Access: Full admin dashboard at `/admin/dashboard`

**Regular User Accounts:**

- Email: `sarah@example.com` | Password: `password123`
- Email: `john@example.com` | Password: `password123`
- Email: `mary@example.com` | Password: `password123`

### 3. Explore the Features

#### For Regular Users:

1. **Browse Prayer Feed** - View all community prayer requests
2. **Submit Prayer Request** - Click "New Prayer" to share your need
3. **Pray for Others** - Click "I Prayed For This" on any request
4. **Leave Encouragement** - Share uplifting messages and Bible verses
5. **View Answered Prayers** - See testimonies of God's faithfulness
6. **Advent Reflections** - Daily scripture and prayer prompts
7. **Community Impact** - See statistics of collective prayer

#### For Admin Users:

1. **Admin Dashboard** - `/admin/dashboard`
2. **Moderate Content** - Review and manage prayer requests
3. **Handle Reports** - Review flagged content
4. **Manage Users** - User administration
5. **Set Featured Prayer** - Highlight a daily prayer request

## 🎨 Design Highlights

- **Sleek & Modern**: Clean Tailwind CSS design with minimal gradients
- **Smooth Animations**: Subtle hover effects and transitions
- **Fully Responsive**: Works beautifully on all devices
- **Accessible**: Easy-to-read fonts and clear navigation
- **Christmas Theme**: Festive colors (emerald green, gold accents)

## 📁 Project Structure

```
pray_noel/
├── app/
│   ├── models.py              # Database models (User, PrayerRequest, Prayer, etc.)
│   ├── forms.py               # WTForms for validation
│   ├── routes/
│   │   ├── auth.py           # Login/Register
│   │   ├── main.py           # Home, About, Community Impact
│   │   ├── prayers.py        # Prayer CRUD operations
│   │   └── admin.py          # Admin panel
│   └── templates/
│       ├── base.html         # Base template with nav & footer
│       ├── index.html        # Beautiful home page
│       ├── auth/             # Login/register pages
│       ├── prayers/          # Prayer feed, create, view, etc.
│       └── admin/            # Admin dashboard
├── config.py                  # App configuration
├── run.py                     # Start the app
├── seed_data.py              # Populate sample data
└── README.md                  # Full documentation
```

## 🔧 Managing the App

### Stop the Server

Press `CTRL + C` in the terminal where Flask is running

### Start the Server

```bash
python run.py
```

### Reset Database with Sample Data

```bash
python seed_data.py
```

### Access Different Pages

- Home: `http://localhost:5000/`
- Prayer Feed: `http://localhost:5000/prayers/feed`
- Create Request: `http://localhost:5000/prayers/create` (login required)
- Answered Prayers: `http://localhost:5000/prayers/answered`
- Advent: `http://localhost:5000/advent`
- Community Impact: `http://localhost:5000/community-impact`
- Admin Dashboard: `http://localhost:5000/admin/dashboard` (admin only)

## ✨ Key Features Implemented

### ✅ Core Features (Complete)

- [x] Prayer request submission with categories
- [x] "Prayed For You" button with prayer counts
- [x] Encouragement messages with Bible verses
- [x] Anonymous and private prayer options
- [x] Admin moderation dashboard
- [x] Content reporting system

### ✅ Community Features (Complete)

- [x] Prayer feed with filters (category, sort)
- [x] Answered prayers section with testimonies
- [x] Daily featured prayer capability
- [x] Community impact statistics page
- [x] Personal dashboards (My Requests, My Prayers)

### ✅ Faith Features (Complete)

- [x] Advent reflections system (Dec 1-25)
- [x] Christmas Eve prayer countdown
- [x] Scripture integration throughout
- [x] Testimony sharing for answered prayers

### ✅ Design (Complete)

- [x] Tailwind CSS for sleek, modern UI
- [x] Smooth hover effects and transitions
- [x] Minimal gradient usage
- [x] Fully responsive design
- [x] Christmas-themed color scheme

### 🔄 Features for Future Enhancement

- [ ] Email notifications
- [ ] Prayer reminders
- [ ] Private prayer circles
- [ ] Audio prayer notes
- [ ] Prayer tree visualization
- [ ] Multilingual support

## 🙏 Sample Data Included

The database includes:

- **6 users** (1 admin, 5 regular users)
- **8 prayer requests** across all categories
- **14 prayers** offered by users
- **3 encouragement messages** with Bible verses
- **5 advent reflections** (days 1, 2, 3, 24, 25)

## 🛠️ Troubleshooting

### Port Already in Use

If port 5000 is busy, edit `run.py` and change the port:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Database Issues

Delete `pray_noel.db` and run `python seed_data.py` again

### Import Errors

Make sure you're in the virtual environment:

```bash
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
```

## 📖 Bible Verses Used

Throughout the app, you'll find encouraging scriptures like:

- Matthew 18:20 - "For where two or three gather..."
- Philippians 4:6 - "Do not be anxious about anything..."
- James 5:16 - "The prayer of a righteous person..."
- Luke 2:11 - "Today in the town of David a Savior has been born..."

## 🎁 Next Steps

1. **Customize Content**: Edit welcome messages, add your own Bible verses
2. **Add More Advent Reflections**: Complete all 25 days in the database
3. **Invite Users**: Share the platform with your church or community
4. **Deploy**: Consider deploying to Heroku, PythonAnywhere, or Azure
5. **Enhance Features**: Add the future features listed above

## 💡 Tips

- Use the **"Urgent"** flag for prayer requests needing immediate attention
- **Anonymous submissions** help people share sensitive requests
- **Private requests** are only accessible via direct link
- Admin can **hide inappropriate content** without deleting
- **Answered prayers** section encourages the community with testimonies

---

**"The prayer of a righteous person is powerful and effective." - James 5:16**

Enjoy using Pray Noel! May it be a blessing to your community. 🙏✨
