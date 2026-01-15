from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from app.models import db, PrayerRequest, User, Report, DailyFeaturedPrayer, AdventReflection
from datetime import date, datetime

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You need administrator privileges to access this page.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Get pending reports
    pending_reports = Report.query.filter_by(status='pending').count()
    
    # Get recent requests
    recent_requests = PrayerRequest.query.order_by(
        PrayerRequest.created_at.desc()
    ).limit(10).all()
    
    # Get stats
    total_users = User.query.count()
    total_requests = PrayerRequest.query.count()
    
    return render_template('admin/dashboard.html',
                         pending_reports=pending_reports,
                         recent_requests=recent_requests,
                         total_users=total_users,
                         total_requests=total_requests)

@bp.route('/reports')
@login_required
@admin_required
def reports():
    status = request.args.get('status', 'pending')
    
    reports = Report.query.filter_by(status=status).order_by(
        Report.created_at.desc()
    ).all()
    
    return render_template('admin/reports.html', reports=reports, current_status=status)

@bp.route('/report/<int:id>/review', methods=['POST'])
@login_required
@admin_required
def review_report(id):
    report = Report.query.get_or_404(id)
    action = request.form.get('action')
    
    if action == 'dismiss':
        report.status = 'dismissed'
        db.session.commit()
        flash('Report dismissed.', 'info')
    elif action == 'remove':
        # Mark request as not public
        report.request.is_public = False
        report.status = 'reviewed'
        db.session.commit()
        flash('Prayer request removed from public view.', 'success')
    
    return redirect(url_for('admin.reports'))

@bp.route('/requests')
@login_required
@admin_required
def requests():
    page = request.args.get('page', 1, type=int)
    
    requests = PrayerRequest.query.order_by(
        PrayerRequest.created_at.desc()
    ).paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/requests.html', requests=requests)

@bp.route('/request/<int:id>/toggle-public', methods=['POST'])
@login_required
@admin_required
def toggle_public(id):
    prayer_request = PrayerRequest.query.get_or_404(id)
    prayer_request.is_public = not prayer_request.is_public
    
    db.session.commit()
    
    status = 'public' if prayer_request.is_public else 'hidden'
    flash(f'Request is now {status}.', 'success')
    
    return redirect(url_for('admin.requests'))

@bp.route('/featured-prayer', methods=['GET', 'POST'])
@login_required
@admin_required
def featured_prayer():
    if request.method == 'POST':
        request_id = request.form.get('request_id')
        feature_date = request.form.get('date')
        
        if not request_id or not feature_date:
            flash('Please provide both request ID and date.', 'error')
            return redirect(url_for('admin.featured_prayer'))
        
        # Parse date
        try:
            feature_date = datetime.strptime(feature_date, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format.', 'error')
            return redirect(url_for('admin.featured_prayer'))
        
        # Check if already featured for that date
        existing = DailyFeaturedPrayer.query.filter_by(date=feature_date).first()
        if existing:
            existing.request_id = request_id
        else:
            featured = DailyFeaturedPrayer(
                request_id=request_id,
                date=feature_date
            )
            db.session.add(featured)
        
        db.session.commit()
        flash('Featured prayer set successfully.', 'success')
        return redirect(url_for('admin.featured_prayer'))
    
    # Get featured prayers
    featured_prayers = DailyFeaturedPrayer.query.order_by(
        DailyFeaturedPrayer.date.desc()
    ).limit(30).all()
    
    # Get recent requests for selection
    recent_requests = PrayerRequest.query.filter_by(
        is_public=True
    ).order_by(PrayerRequest.created_at.desc()).limit(20).all()
    
    return render_template('admin/featured_prayer.html',
                         featured_prayers=featured_prayers,
                         recent_requests=recent_requests)

@bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@bp.route('/user/<int:id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(id):
    user = User.query.get_or_404(id)
    
    # Don't allow removing own admin status
    if user.id == current_user.id:
        flash('You cannot modify your own admin status.', 'error')
        return redirect(url_for('admin.users'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    
    status = 'granted' if user.is_admin else 'revoked'
    flash(f'Admin privileges {status} for {user.username}.', 'success')
    
    return redirect(url_for('admin.users'))
