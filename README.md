# Pray Noel - Christmas Prayer Request Platform

A faith-based community platform where people submit prayer requests, receive support through prayers and encouragement, and share testimonies of answered prayers.

## Features

### Core Features

- **Prayer Request Submission**: Users can submit detailed prayer requests with categories, Bible verses, and privacy options
- **"Prayed For You" Action**: One-click prayer acknowledgment with optional prayer notes
- **Encouragement & Scripture Replies**: Community members can leave encouraging messages and Bible verses
- **Moderation & Safety**: Admin dashboard for content moderation and reporting system

### Community Features

- **Prayer Feed**: Browse prayer requests with category and sort filters
- **Answered Prayers Section**: Testimonies of God's faithfulness
- **Daily Featured Prayer**: Highlighted community prayer request
- **Prayer Statistics**: Track prayers offered and community impact
- **Personal Dashboard**: View your prayer requests and prayers offered

### Faith-Enhancing Features

- **Advent Reflections**: Daily scripture readings and prayer prompts (December 1-25)
- **Christmas Eve Global Prayer**: Countdown to unified prayer moment
- **Community Impact Page**: Statistics showing the power of collective prayer

### Design

- Clean, modern interface using Tailwind CSS
- Smooth animations and transitions
- Minimal gradient usage for elegant, reverent design
- Fully responsive for mobile and desktop

## Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Authentication**: Flask-Login with secure password hashing

## Installation

1. **Clone or navigate to the project directory**

   ```bash
   cd pray_noel
   ```

2. **Virtual environment is already set up**
   The virtual environment is located in `.venv` directory

3. **Activate virtual environment** (if not already active)

   ```bash
   # On Windows
   .venv\Scripts\activate

   # On macOS/Linux
   source .venv/bin/activate
   ```

4. **Install dependencies** (already installed)
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Flask server**

   ```bash
   python run.py
   ```

2. **Access the application**
   Open your browser and navigate to:

   ```
   http://localhost:5000
   ```

3. **Create an account**
   - Click "Sign Up" to create your account
   - Login with your credentials
   - Start submitting prayer requests or praying for others!

## First Steps

1. **Create an Admin Account**

   - Register a new account
   - Manually set `is_admin=True` in the database for your user
   - Access admin dashboard at `/admin/dashboard`

2. **Submit Your First Prayer Request**

   - Click "New Prayer" button
   - Fill in the title, category, and description
   - Choose privacy options
   - Submit and share with the community

3. **Pray for Others**
   - Browse the Prayer Feed
   - Click "I Prayed For This" button
   - Optionally leave a prayer note or encouragement

## Project Structure

```
pray_noel/
├── app/
│   ├── __init__.py           # App factory
│   ├── models.py             # Database models
│   ├── forms.py              # WTForms
│   ├── routes/
│   │   ├── auth.py           # Authentication routes
│   │   ├── main.py           # Main pages routes
│   │   ├── prayers.py        # Prayer request routes
│   │   └── admin.py          # Admin routes
│   ├── templates/            # HTML templates
│   │   ├── base.html         # Base template
│   │   ├── index.html        # Home page
│   │   ├── auth/             # Auth templates
│   │   ├── prayers/          # Prayer templates
│   │   └── admin/            # Admin templates
│   └── static/               # Static files
│       ├── css/
│       └── js/
├── config.py                 # Configuration
├── run.py                    # Application entry point
├── requirements.txt          # Dependencies
├── .env                      # Environment variables
└── README.md                 # This file
```

## Database Models

- **User**: User accounts with authentication
- **PrayerRequest**: Prayer requests with categories and privacy options
- **Prayer**: Prayer acknowledgments with optional notes
- **Encouragement**: Encouraging messages with optional Bible verses
- **Report**: Content moderation reports
- **PrayerCircle**: Private prayer groups
- **AdventReflection**: Daily advent devotions
- **DailyFeaturedPrayer**: Featured prayer of the day
- **PrayerStats**: User prayer statistics

## Environment Variables

Create a `.env` file with:

```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///pray_noel.db
```

## Features Coming Soon

- Email notifications for prayer updates
- Prayer reminders system
- Prayer circles (private groups)
- Audio prayer options
- Multilingual support
- Prayer tree visualization
- Mobile app

## Safety & Moderation

- All content can be reported by users
- Admin approval system for prayer requests
- Keyword filtering for inappropriate content
- Privacy controls for sensitive requests
- Option for anonymous submissions

## Contributing

This is a faith-based community project. Contributions are welcome!

## License

This project is created for the glory of God and to support the prayer community.

## Support

For questions or support, please contact the admin team.

---

**"For where two or three gather in my name, there am I with them." - Matthew 18:20**

Made with ❤️ for the glory of God
