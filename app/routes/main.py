from flask import Blueprint, render_template
from app.models import db, PrayerRequest, DailyFeaturedPrayer, Prayer
from datetime import datetime, date
from sqlalchemy import func, desc

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # Get featured prayer of the day
    today = date.today()
    featured = DailyFeaturedPrayer.query.filter_by(date=today).first()
    featured_request = featured.prayer_request if featured else None
    
    # Get recent prayer requests (approved only)
    recent_requests = PrayerRequest.query.filter_by(
        is_public=True,
        is_private=False
    ).order_by(desc(PrayerRequest.created_at)).limit(6).all()
    
    # Get community stats
    total_prayers = Prayer.query.count()
    total_requests = PrayerRequest.query.filter_by(is_public=True).count()
    answered_prayers = PrayerRequest.query.filter_by(is_answered=True).count()
    
    return render_template('index.html',
                         featured_request=featured_request,
                         recent_requests=recent_requests,
                         total_prayers=total_prayers,
                         total_requests=total_requests,
                         answered_prayers=answered_prayers)

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/community-impact')
def community_impact():
    # Total prayers offered
    total_prayers = Prayer.query.count()
    
    # Total requests
    total_requests = PrayerRequest.query.filter_by(is_public=True).count()
    
    # Answered prayers
    answered_prayers = PrayerRequest.query.filter_by(is_answered=True).count()
    
    # Category breakdown
    category_stats = db.session.query(
        PrayerRequest.category,
        func.count(PrayerRequest.id).label('count')
    ).filter_by(is_public=True).group_by(PrayerRequest.category).all()
    
    # Most prayed for today
    today = date.today()
    most_prayed_today = db.session.query(
        PrayerRequest,
        func.count(Prayer.id).label('prayer_count')
    ).join(Prayer).filter(
        func.date(Prayer.created_at) == today,
        PrayerRequest.is_public == True
    ).group_by(PrayerRequest.id).order_by(desc('prayer_count')).limit(5).all()
    
    return render_template('community_impact.html',
                         total_prayers=total_prayers,
                         total_requests=total_requests,
                         answered_prayers=answered_prayers,
                         category_stats=category_stats,
                         most_prayed_today=most_prayed_today)

@bp.route('/advent')
def advent():
    from app.models import AdventReflection
    
    # Get current day (1-25 for December)
    current_day = datetime.now().day
    if datetime.now().month != 12:
        current_day = 1
    
    # Get all reflections up to current day
    reflections = AdventReflection.query.filter(
        AdventReflection.day <= current_day
    ).order_by(AdventReflection.day).all()
    
    # Get today's reflection
    today_reflection = AdventReflection.query.filter_by(day=current_day).first()
    
    return render_template('advent.html',
                         reflections=reflections,
                         today_reflection=today_reflection,
                         current_day=current_day)

@bp.route('/christmas-eve')
def christmas_eve():
    from config import Config
    prayer_time = Config.CHRISTMAS_EVE_PRAYER_TIME
    
    return render_template('christmas_eve.html', prayer_time=prayer_time)

@bp.route('/prayer-tree')
def prayer_tree():
    # Get total prayers
    total_prayers = Prayer.query.count()
    
    # Get category breakdown
    category_counts = {}
    for category in ['Family', 'Health', 'Finances', 'Relationships', 'Grief', 'Gratitude']:
        count = db.session.query(func.count(Prayer.id)).join(PrayerRequest).filter(
            PrayerRequest.category == category
        ).scalar()
        category_counts[category] = count or 0
    
    return render_template('prayer_tree.html',
                         total_prayers=total_prayers,
                         category_counts=category_counts)
