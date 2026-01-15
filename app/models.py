from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    prayer_requests = db.relationship('PrayerRequest', backref='author', lazy=True, foreign_keys='PrayerRequest.user_id')
    prayers = db.relationship('Prayer', backref='user', lazy=True)
    encouragements = db.relationship('Encouragement', backref='author', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class PrayerRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Family, Health, Finances, Relationships, Grief, Gratitude
    bible_verse = db.Column(db.Text, nullable=True)
    is_anonymous = db.Column(db.Boolean, default=False)
    is_private = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=True)  # Admin approved
    is_urgent = db.Column(db.Boolean, default=False)
    is_answered = db.Column(db.Boolean, default=False)
    testimony = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    prayers = db.relationship('Prayer', backref='request', lazy=True, cascade='all, delete-orphan')
    encouragements = db.relationship('Encouragement', backref='request', lazy=True, cascade='all, delete-orphan')
    reports = db.relationship('Report', backref='request', lazy=True, cascade='all, delete-orphan')
    
    @property
    def prayer_count(self):
        return len(self.prayers)
    
    @property
    def display_name(self):
        if self.is_anonymous:
            return "Anonymous"
        return self.author.username

class Prayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('prayer_request.id'), nullable=False)
    prayer_note = db.Column(db.Text, nullable=True)
    is_private = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Encouragement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('prayer_request.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    bible_verse = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('prayer_request.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, reviewed, dismissed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    reporter = db.relationship('User', backref='reports')

class PrayerCircle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    invite_code = db.Column(db.String(20), unique=True, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    members = db.relationship('CircleMember', backref='circle', lazy=True, cascade='all, delete-orphan')
    requests = db.relationship('CircleRequest', backref='circle', lazy=True, cascade='all, delete-orphan')
    
    creator = db.relationship('User', backref='created_circles')

class CircleMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    circle_id = db.Column(db.Integer, db.ForeignKey('prayer_circle.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='circle_memberships')

class CircleRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    circle_id = db.Column(db.Integer, db.ForeignKey('prayer_circle.id'), nullable=False)
    request_id = db.Column(db.Integer, db.ForeignKey('prayer_request.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    prayer_request = db.relationship('PrayerRequest', backref='circle_requests')

class AdventReflection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False, unique=True)  # 1-25
    scripture = db.Column(db.Text, nullable=False)
    reflection = db.Column(db.Text, nullable=False)
    prompt = db.Column(db.Text, nullable=False)

class DailyFeaturedPrayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('prayer_request.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    prayer_request = db.relationship('PrayerRequest', backref='featured_dates')

class PrayerStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    prayers_offered = db.Column(db.Integer, default=0)
    
    user = db.relationship('User', backref='prayer_stats')
